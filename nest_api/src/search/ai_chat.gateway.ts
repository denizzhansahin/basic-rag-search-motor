// nest_api/src/ai_chat.gateway.ts
import { WebSocketGateway, WebSocketServer, SubscribeMessage, MessageBody, ConnectedSocket, OnGatewayDisconnect } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Redis } from 'ioredis';
import { randomUUID } from 'crypto';

@WebSocketGateway({ cors: { origin: '*' } })
export class AiChatGateway implements OnGatewayDisconnect{
  @WebSocketServer() server: Server;
  
  private redisPub = new Redis(process.env.REDIS_URL || 'redis://redis_broker:6379');
  private redisSub = new Redis(process.env.REDIS_URL || 'redis://redis_broker:6379');

  // 2. KULLANICI İŞ TAKİP HARİTASI (RAM'de tutulur)
  private activeJobs = new Map<string, string>(); // client.id -> jobId

  // 3. BAĞLANTI KOPARSA ÇALIŞACAK FONKSİYON (Sayfa yenileme, sekmeyi kapatma)
  handleDisconnect(client: Socket) {
    const activeJobId = this.activeJobs.get(client.id);
    if (activeJobId) {
      console.log(`🔌 Kullanıcı koptu, arka plan işlemi iptal ediliyor: ${activeJobId}`);
      this.redisPub.publish('cancel_jobs', activeJobId); // Python'a iptal sinyali ateşle
      this.activeJobs.delete(client.id);
    }
  }

  @SubscribeMessage('send_ai_message')
  async handleAiMessage(@MessageBody() data: any, @ConnectedSocket() client: Socket) {
    
// 4. EĞER KULLANICI ESKİSİ BİTMEDEN YENİ SORU SORDUYSA, ESKİSİNİ İPTAL ET
    const prevJobId = this.activeJobs.get(client.id);
    if (prevJobId) {
      console.log(`🛑 Yeni istek geldi, eski işlem iptal ediliyor: ${prevJobId}`);
      this.redisPub.publish('cancel_jobs', prevJobId);
    }

    // 1. SOHBET LİMİTİ KONTROLÜ (Maksimum 30 Mesaj)
    // History dizisindeki her obje 1 mesajdır.
    if (data.history && data.history.length >= 30) {
      client.emit('ai_chat_error', { message: 'Sohbet limitine (10 mesaj) ulaştınız. Lütfen yeni bir sohbet başlatın.' });
      return;
    }

    // 2. DOSYA KONTROLÜ (Tür ve Boyut)
    if (data.fileBase64) {
      // Base64 string'in bellekteki byte boyutunu yaklaşık hesaplama
      const sizeInBytes = Math.ceil((data.fileBase64.length * 3) / 4);
      if (sizeInBytes > 500 * 1024) { // 500 KB
         client.emit('ai_chat_error', { message: 'Dosya boyutu 500KB sınırını aşıyor!' });
         return;
      }

      // Dosya türü kontrolü
      const allowedTypes = ['image/png', 'image/jpeg', 'image/webp', 'application/pdf', 'text/plain'];
      if (!allowedTypes.includes(data.fileType)) {
         client.emit('ai_chat_error', { message: 'Sadece resim, PDF veya TXT dosyaları yüklenebilir.' });
         return;
      }
    }

    const jobId = randomUUID();
    // 5. YENİ İŞİ HARİTAYA KAYDET
    this.activeJobs.set(client.id, jobId);
    console.log(`🤖 [AI CHAT] Yeni mesaj: ${data.query.substring(0,20)}... | ID: ${jobId}`);
    
    // Yanıtı dinle ve React'a ilet
    this.redisSub.subscribe(`job:${jobId}`);
    this.redisSub.on('message', (channel, message) => {
      if (channel === `job:${jobId}`) {
        const response = JSON.parse(message);
        
        // 6. İŞLEM BİTTİYSE VEYA HATA VERDİYSE HARİTADAN SİL
        if (response.type === 'DONE' || response.type === 'ERROR') {
          if (this.activeJobs.get(client.id) === jobId) {
            this.activeJobs.delete(client.id);
          }
          this.redisSub.unsubscribe(`job:${jobId}`);
        } else {
          client.emit('ai_chat_response', response);
        }
      }
    });

    // İşi Redis'e yolla (Yeni iş tipi: ai_chat)
    const jobData = {
      jobId,
      type: 'ai_chat',
      query: data.query,
      history: data.history || [],
      fileBase64: data.fileBase64,
      fileType: data.fileType
    };
    await this.redisPub.lpush('task_queue', JSON.stringify(jobData));
  }
}