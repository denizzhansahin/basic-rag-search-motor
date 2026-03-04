import { Test, TestingModule } from '@nestjs/testing';
import { SearchGateway } from './search.gateway';

describe('SearchGateway', () => {
  let gateway: SearchGateway;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [SearchGateway],
    }).compile();

    gateway = module.get<SearchGateway>(SearchGateway);
  });

  it('should be defined', () => {
    expect(gateway).toBeDefined();
  });
});
