import { Module } from '@nestjs/common';
import { RedisGateway } from './redis.gateway';
import { SearchGateway } from './search.gateway';

@Module({
  providers: [
    process.env.REDIS_URL ? RedisGateway : SearchGateway
  ],
})
export class SearchModule {}
