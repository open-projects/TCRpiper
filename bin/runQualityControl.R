args = commandArgs(trailingOnly=TRUE)
sample_info_file = './sample_info_GE21.txt'#args[1]
out_dir = './runQC/'#args[2]


library(ggplot2)
library(data.table)
library(dplyr)

s = fread(sample_info_file)

################### checkout #############
checkout_file = paste("checkout/checkout.log.txt",sep="")
d<-fread(checkout_file)
colnames(d)[1] = "INPUT_FILE_1"
d_sum = d %>% group_by(INPUT_FILE_1) %>% summarise(total = sum(MASTER),
                                           total_undef = sum(MASTER[SAMPLE %in% c("undef-m","undef-s")]),
                                           file_samples = paste(SAMPLE[!(SAMPLE %in% c("undef-m","undef-s"))],collapse = "\n")) %>% 
          mutate(p_undef = total_undef/total)

cond<-d_sum$p_undef>0.2

max_reads = max(d_sum$total)
p1 = ggplot(d_sum,aes(total,p_undef,color=INPUT_FILE_1))+geom_point()+
  geom_text(data = d_sum[cond,],aes(label=file_samples),vjust = 1.5, show.legend=F)+
  theme_bw()+theme(legend.position="bottom",legend.text =  element_text(size=10))+xlab("Total observed reads")+ylab("% of reads without barcodes\n(undef-m,s)")+
  scale_y_continuous(limits = c(0,1))+scale_x_continuous(limits = c(0-0.1*max_reads,max_reads*(1+0.1)))


############# reads #####################

m = merge(d, s, by.x = "SAMPLE",by.y = "sample_name")

cond<-(m$reads.exp>m$MASTER*5)|(m$reads.exp<m$MASTER/5)
sum_p<-sum(m$MASTER)/sum(m$reads.exp)

max_reads<-max(max(m$reads.exp),max(m$MASTER))
min_reads<-min(min(m$reads.exp),min(m$MASTER))

max_log10<-10^ceiling(log10(max_reads))
min_log10<-10^floor(log10(min_reads))

p2 = ggplot(m,aes(reads.exp,MASTER,color=chain))+geom_point()+
  theme_bw()+theme(legend.position="bottom")+
  geom_text(data=m[cond,],aes(label=SAMPLE), vjust = -1,hjust=0.5,show.legend=F)+
  scale_x_log10(limits=c(min_log10,max_log10))+scale_y_log10(limits=c(min_log10,max_log10))+ylab("reads OBSERVED")+xlab("reads EXPECTED")+
  annotate("text", x = min_log10, y = max_log10, label= paste("sum.reads.obs/sum.reads.exp =",round(sum_p,2)),hjust=0) 

################ assemble ###########
assemble_file = paste("assemble/assemble.log.txt",sep="")

a<-fread(assemble_file)
colnames(a)[1] = "SAMPLE_ID"

r<-merge(a,s,by.x="SAMPLE_ID",by.y="sample_name")

cond<-r$READS_GOOD_TOTAL<0.8*r$READS_TOTAL
max_reads<-max(r$READS_TOTAL)
min_reads<-min(r$READS_GOOD_TOTAL)

p3 = ggplot(r,aes(READS_TOTAL,READS_GOOD_TOTAL,color=chain))+geom_point(aes(size=MIG_COUNT_THRESHOLD),alpha=0.7)+
  geom_text(data=r[cond,],aes(label=SAMPLE_ID), vjust = -1,hjust=0.5,show.legend=F)+
  xlim(0,max_reads)+ylim(0,max_reads)+
  theme_bw()+theme(legend.position="bottom")

################ alignment ###########
report_path = paste("analyze",sep="")

files <- list.files(path=report_path,pattern = ".report")
df<-data.frame(names=character(),pp=numeric())
for (f in files){
  con <- file(paste(report_path,"/",f,sep=""), "r", blocking = FALSE)
  rl<-readLines(con) # empty
  name<-sub(".report", "", f)
  name<-sub(".txt", "", name)
  p<-as.numeric(strsplit(strsplit(rl[8],"\\(")[[1]][2],"%")[[1]][1])
  close(con)
  #df1<-data.frame(names=name,pp=p)
  df<-rbind(df,data.frame(names=name,pp=p))
}
ar<-merge(df,s,by.x="names",by.y="sample_name")

p4 = ggplot(ar,aes("samples",pp,color=chain))+geom_jitter(height=0,width=0.1)+theme_bw()+
  theme(legend.position="bottom")+ylab("Successfully aligned reads, %")+xlab("")+ylim(0,100)

ggsave(paste(out_dir,"/","barcodes.pdf",sep=""),p1,height = 6, width = 6)
ggsave(paste(out_dir,"/","reads.pdf",sep=""),p2,height = 6, width = 6)
ggsave(paste(out_dir,"/","migs.pdf",sep=""),p3,height = 6, width = 6)
ggsave(paste(out_dir,"/","alinments.pdf",sep=""),p4,height = 6, width = 6)
