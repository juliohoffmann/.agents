import { PrismaClient } from '@prisma/client';
import { MongoClient } from 'mongodb';
import { PrismaMongoClient } from '@prisma/adapter-mongodb';

const mongoUrl = process.env.MONGO_URL || 'mongodb://admin:123456@db_mongo:27017/db_mongo?authSource=admin';
const mongoClient = new MongoClient(mongoUrl);
const adapter = new PrismaMongoClient(mongoClient);

export const prisma = new PrismaClient({ adapter });

export async function connectToPrisma() {
  await mongoClient.connect();
  console.log('Conectado ao MongoDB via Prisma');
}