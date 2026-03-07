import { Module } from '@nestjs/common';
import { RedisGateway } from './redis.gateway';
import { SearchGateway } from './search.gateway';
import { AiChatGateway } from './ai_chat.gateway';

@Module({
  providers: [
    process.env.REDIS_URL ? RedisGateway : SearchGateway,
    AiChatGateway
  ],
})
export class SearchModule {}
