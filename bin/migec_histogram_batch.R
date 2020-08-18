#
# Plots a fancy oversequencing histogram from tables pre-computed by Histogram util
#
# usage:
# $cd histogram_output_dir/
# $RScript histogram.R
#
args = commandArgs(trailingOnly=TRUE)
dir = args[1]
print(dir)
library(reshape2)
library(ggplot2)
#dir<-"histogram/"
require(ggplot2); require(reshape)

build_df <- function(dir,stat, units, ind, sweep_df = NULL) {
  df<- read.table(paste(dir,'/',stat, units, ".txt", sep= ""), header=FALSE, comment="", sep = "\t")
df<-df[c(1,(ind+1)),]
  x<-df[1,3:ncol(df)]
  id<-df[2:nrow(df), 1] 
  
  if (is.null(sweep_df)) {
    sweep_df <- df
  }
  
  df[2:nrow(df),3:ncol(df)] <- sweep(df[2:nrow(df),3:ncol(df)], 1, rowSums(sweep_df[2:nrow(df),3:ncol(df)]), FUN = "/")
  
  df.m <- melt(df[2:nrow(df), c(1,3:ncol(df))])
  df.m$x <- as.vector(t(x[df.m$variable]))
  df.m$s <- rep(stat, nrow(df.m))
  list(sweep_df, df.m,id)
}

for (ind in c(1:100)){
for (units in c("", "-units")) {  
  dfo <- build_df(dir,"overseq", units, ind)
  dfc <- build_df(dir,"collision1", units, ind, dfo[[1]])     
  df <- rbind(dfo[[2]], dfc[[2]])
  id<-dfo[[3]]

  pdf(paste(dir,"/",id,"_histogram", units, ".pdf", sep= ""))
  
  print(
    ggplot(df, aes(x=x,y=value))+geom_smooth()+
      scale_x_log10(name = "MIG size, reads", expand=c(0,0), limits=c(1, 10000), breaks = c(1:10,100,1000,10000), labels = c("1", rep("", 8), 10, 100, 1000, 10000), oob=scales::rescale_none)+
      scale_y_continuous(name = "",expand=c(0,0), limits = c(0, max(df$value)), oob=scales::rescale_none)+theme_bw()+theme(panel.grid.minor = element_blank()) + facet_grid(s~.)
  )
  
  dev.off()  
}
}