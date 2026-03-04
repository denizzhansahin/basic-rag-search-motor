import { CanActivate, ExecutionContext, Injectable } from '@nestjs/common';
import { WsException } from '@nestjs/websockets';
import { Socket } from 'socket.io';

@Injectable()
export class WsThrottlerGuard implements CanActivate {
  // Kullanıcıların istek sayılarını RAM'de tutacağımız basit bir harita
  private clients = new Map<string, { count: number; expiresAt: number }>();
  
  // KURALLAR
  private readonly LIMIT = 2; // 1 dakika içinde en fazla 5 arama yapılabilir
  private readonly WINDOW_MS = 60000; // 60 saniye (1 dakika)

  canActivate(context: ExecutionContext): boolean {
    const client: Socket = context.switchToWs().getClient();
    
    // Güvenlik için bağlanan kişinin IP adresini alıyoruz
    // (Localhost'ta test ederken genellikle ::1 veya 127.0.0.1 döner)
    const clientIp = client.handshake.address;
    const now = Date.now();

    const record = this.clients.get(clientIp);

    if (record && record.expiresAt > now) {
      if (record.count >= this.LIMIT) {
        // Sınır aşıldıysa, işlemi iptal et ve hata fırlat!
        throw new WsException('Çok fazla arama yaptınız. Lütfen 1 dakika bekleyin.');
      }
      record.count += 1;
    } else {
      // Yeni kullanıcı veya süresi dolmuş kullanıcı için sayacı sıfırla
      this.clients.set(clientIp, { count: 1, expiresAt: now + this.WINDOW_MS });
    }

    return true; // Sorun yoksa işlemin geçmesine izin ver
  }
}