import { UseGuards } from '@nestjs/common';
import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  MessageBody,
  ConnectedSocket,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import * as WebSocket from 'ws';
import { WsThrottlerGuard } from './rate-limit.guard';





@WebSocketGateway({
  cors: { origin: '*', methods: ['GET', 'POST'] },
})
export class SearchGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;


handleConnection(client: Socket) {

  console.log(`🟢 Bağlandı: ${client.id}`);

  const originsEnv = process.env.ALLOWED_ORIGINS || "";

  const allowedOrigins = originsEnv
    .split(",")
    .map(o => o.trim());

  const origin = client.handshake.headers.origin;

  console.log("Origin:", origin);
  console.log("Allowed:", allowedOrigins);

  if (!origin || !allowedOrigins.some(o => origin.startsWith(o))) {

    console.log("❌ Yetkisiz origin:", origin);

    client.disconnect();

    return;
  }

  console.log("✅ Yetkili origin:", origin);
}

  handleDisconnect(client: Socket) {
    console.log(`🔴 Ayrıldı: ${client.id}`);
  }


  @UseGuards(WsThrottlerGuard)
  @SubscribeMessage('takip_sorusu_sor')
  handleTakipSorusu(@MessageBody() data: any, @ConnectedSocket() client: Socket) {
    const pythonWs = new WebSocket(`ws://${process.env.PYTHON_URL}/ws/follow-up?token=${process.env.SECRET_KEY}`);

    // ✅ Kullanıcı çıkarsa Python WS kapat
    client.once('disconnect', () => {
      console.log("🔴 Kullanıcı gitti → Python WS kapatılıyor");
      pythonWs.close();
    });

    pythonWs.on('open', () => {
      pythonWs.send(JSON.stringify(data));
    });

    pythonWs.on('message', (msg) => {
      try {
        const res = JSON.parse(msg.toString());
        client.emit('takip_cevabi', res);

        // ✅ ÇOK ÖNEMLİ: İşlem bitti, Python bağlantısını kapat!
        pythonWs.close();
      } catch (e) {
        console.error("❌ Veri işlenirken hata:", e);
        pythonWs.close(); // Hata olsa da kapat
      }
    });

    pythonWs.on('error', (err) => {
      console.error("❌ Python WS Hatası:", err);
      pythonWs.close(); // Hata durumunda bağlantıyı temizle
    });
  }

  @UseGuards(WsThrottlerGuard)
  @SubscribeMessage('arama_yap')
  handleSearch(
    @MessageBody() data: { query: string; page?: number; limit?: number },
    @ConnectedSocket() client: Socket,
  ) {
    const page = data.page || 1;
    const limit = data.limit || 10;

    console.log(`🔎 Sorgu: "${data.query}" | Python'a iletiliyor...`);

    const pythonWsUrl = `ws://${process.env.PYTHON_URL}/ws/search?token=${process.env.SECRET_KEY}`;
    const pythonWs = new WebSocket(pythonWsUrl);

    // ✅ Kullanıcı çıkarsa Python WS kapat
    client.once('disconnect', () => {
      console.log("🔴 Kullanıcı gitti → Python WS kapatılıyor");
      pythonWs.close();
    });

    pythonWs.on('open', () => {
      pythonWs.send(JSON.stringify({ query: data.query, page: page, limit: limit }));
    });

    // BURASI ÇOK ÖNEMLİ: Python'dan gelen veriyi dinlediğimiz yer
    pythonWs.on('message', (message: WebSocket.RawData) => {
      try {
        const response = JSON.parse(message.toString());
        console.log(`📦 [NestJS] Python'dan veri geldi! TİP: ${response.type}`); // İZLEME LOGU

        if (response.type === 'FULL_RESULTS' || response.type === 'AI_RESULTS') {
          client.emit('arama_sonucu', response);
          console.log(`✅ [NestJS] Veri React'a başarıyla fırlatıldı.`);
        }
        else if (response.type === 'DONE') {
          client.emit('islem_bitti', { status: 'success' });
          pythonWs.close();
        }
        else if (response.type === 'ERROR') {
          client.emit('hata', { message: response.message });
        }
      } catch (error) {
        console.error("❌ [NestJS] JSON Parçalama Hatası! Gelen veri bozuk olabilir:", error);
      }
    });

    pythonWs.on('error', (err) => {
      console.error('❌ Python sunucusuna ulaşılamadı:', err);
      client.emit('hata', { message: 'Yapay zeka motoruna ulaşılamıyor.' });
    });
  }
}