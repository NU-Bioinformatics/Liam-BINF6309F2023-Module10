#!/usr/bin/env Rscript

m <- as.matrix(read.table("ibd_view.mdist"))
mds <- cmdscale(as.dist(1-m))
k <- c( rep("green",45) , rep("blue",44) )
plot1 <- plot(mds,pch=20,col=k)
ggsave("my_plot.png", plot = plot1, width = 6, height = 4, dpi = 300)

# simple regression
d <- read.table("rec_snp1.recode.raw" , header=T)
summary(glm(PHENOTYPE-1 ~ rs2222162_A, data=d, family="binomial"))