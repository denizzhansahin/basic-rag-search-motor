import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { IoAdapter } from '@nestjs/platform-socket.io';
import { ServerOptions } from 'socket.io';
import { createAdapter } from '@socket.io/redis-adapter';
import { Redis } from 'ioredis';

// 1. REDIS ADAPTER SINIFI
export class RedisIoAdapter extends IoAdapter {
  private adapterConstructor: ReturnType<typeof createAdapter>;

  async connectToRedis(): Promise<void> {
    // Ortam değişkeninden URL'yi alıyoruz (Docker için redis_broker, Local için localhost)
    const redisUrl = process.env.REDIS_URL || 'redis://localhost:6379';
    
    const pubClient = new Redis(redisUrl);
    const subClient = pubClient.duplicate();

    // Bağlantı hatalarını izlemek için (Opsiyonel ama önerilir)
    pubClient.on('error', (err) => console.error('Redis Pub Error', err));
    subClient.on('error', (err) => console.error('Redis Sub Error', err));

    this.adapterConstructor = createAdapter(pubClient, subClient);
  }

  createIOServer(port: number, options?: ServerOptions): any {
    const server = super.createIOServer(port, options);
    server.adapter(this.adapterConstructor);
    return server;
  }
}

// 2. BOOTSTRAP (BAŞLATICI)
async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // --- KRİTİK EKLEME: Redis Adapter'ı Aktifleştirme ---
  const redisIoAdapter = new RedisIoAdapter(app);
  try {
    await redisIoAdapter.connectToRedis();
    app.useWebSocketAdapter(redisIoAdapter);
    console.log('✅ Redis Adapter başarıyla bağlandı.');
  } catch (error) {
    console.error('❌ Redis Adapter bağlanamadı, standart WebSocket kullanılıyor.', error);
  }
  // --------------------------------------------------

  // CORS ayarlarını unutma (Frontend'in bağlanabilmesi için)
  app.enableCors();

  const port = process.env.PORT || 3000;
  await app.listen(port);
  console.log(`🚀 NestJS ${port} portunda çalışıyor.`);
}

bootstrap();