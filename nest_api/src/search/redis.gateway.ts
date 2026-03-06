import { WebSocketGateway, WebSocketServer, SubscribeMessage, MessageBody, ConnectedSocket } from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Redis } from 'ioredis';
import { randomUUID } from 'crypto';


@WebSocketGateway({ cors: { origin: '*' } })
export class RedisGateway {
  @WebSocketServer() server: Server;
  
  // Docker ağındaki Redis'e bağlan
  private redisPub = new Redis(process.env.REDIS_URL || 'redis://redis_broker:6379');
  private redisSub = new Redis(process.env.REDIS_URL || 'redis://redis_broker:6379');

  

  @SubscribeMessage('arama_yap')
  async handleSearch(@MessageBody() data: { query: string }, @ConnectedSocket() client: Socket) {
    const jobId = randomUUID();
    console.log(`📥 Arama kuyruğa atılıyor: ${data.query} | ID: ${jobId}`);

    this.redisSub.on('message', (channel, message) => {
  console.log(`📩 Redis'ten mesaj geldi! Kanal: ${channel}`); // Bunu ekle
  if (channel === `job:${jobId}`) {
     // ...
  }
});

    // Dinleyici (Worker'dan gelen cevapları React'a ilet)
    this.redisSub.subscribe(`job:${jobId}`);
    this.redisSub.on('message', (channel, message) => {
      if (channel === `job:${jobId}`) {
        const response = JSON.parse(message);
        if (response.type === 'DONE') {
          this.redisSub.unsubscribe(`job:${jobId}`);
        } else {
          client.emit('arama_sonucu', response);
        }
      }
    });

    // İşi Kuyruğa Yaz
    const jobData = { jobId, type: 'search', query: data.query };
    await this.redisPub.lpush('task_queue', JSON.stringify(jobData));
  }

  @SubscribeMessage('takip_sorusu_sor')
  async handleTakip(@MessageBody() data: any, @ConnectedSocket() client: Socket) {
    const jobId = randomUUID();
    
    this.redisSub.subscribe(`job:${jobId}`);
    this.redisSub.on('message', (channel, message) => {
      if (channel === `job:${jobId}`) {
        client.emit('takip_cevabi', JSON.parse(message));
        this.redisSub.unsubscribe(`job:${jobId}`);
      }
    });

    const jobData = { jobId, type: 'follow_up', question: data.question, history: data.history };
    await this.redisPub.lpush('task_queue', JSON.stringify(jobData));
  }
}