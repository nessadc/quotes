##### upgrade #####
ALTER TABLE "quote" DROP COLUMN "url";
##### downgrade #####
ALTER TABLE "quote" ADD "url" TEXT NOT NULL;
