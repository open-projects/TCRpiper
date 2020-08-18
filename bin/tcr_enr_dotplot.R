# Nadia Bykova
# 2019-03-05
# detection of enriched TCR sequences in pos_file over baseline neg_file
# usage: Rscript tcr_enr_dotplot.R [options] pos_file neg_file

########## parse input line ########################
library(optparse) 
# manual: http://cran.r-project.org/web/packages/optparse/optparse.pdf
# vignette: http://www.icesi.edu.co/CRAN/web/packages/optparse/vignettes/optparse.pdf
option_list = list(
  make_option(c("-f", "--freq"), action="store_true", default=FALSE,
              help="type of axis freq , with a default [%default], i.e. count"),
  make_option(c("-l", "--label"), action="store", default=NA, type='character',
              help="type of axis label (e.g. CD137 or TET or whatever), with a default [filenames]"),
  make_option(c("-c", "--clones"), action="store", default="cdr3nt", type='character',
              help="type of clones (cdr3nt or cdr3aa) , with a default [%default]"),
  make_option(c("-o", "--outfile"), action="store", default=NA, type='character',
              help="output file prefix, with a default [dotplot]"),
  make_option(c("-d", "--dir"), action="store", default=NA, type='character',
              help="output directory, with a default [.]"),
  make_option(c("-i", "--in-dir"), action="store", default=NA, type='character',
              help="source directory, with a default [.]"),
  make_option(c("-t", "--threshold"), action="store", default="1e-8", type='numeric',
              help="enrichment p-value threshold (exact Fisher test with BH correction), with a default [%default]"),
  make_option(c("-w", "--wells"), action="store", default=NA, type='numeric',
              help="file with pathways to wells data, with a default [%default]"),
  make_option(c("-v", "--verbose"), action="store_true", default=FALSE,
              help="Should the program print inintial parameters? [%default]")
)
input = parse_args(OptionParser(usage = "Usage: %prog [options] pos_file neg_file\n",option_list=option_list,
                              description = "(both input files should be in VDJ format)"),positional_arguments = 2)
#opt = input$options
#args = input$args
#pos.file = args[1]
#neg.file = args[2]
pos.f = 'nc.vdj.Trizol_pLTI005_HA-1_exp_total_well_tetr_positive_1557.clonotypes.TRA'
pos.file = paste(pos.f, '.txt', sep ='')
neg.f = 'nc.vdj.Trizol_pLTI005_HA-1_exp_total_wel_tetr_neg_1556.clonotypes.TRA'
neg.file = paste(neg.f, '.txt', sep ='')
in_dir = getwd()
if (is.na(opt$i)) {
  in_dir = getwd()
} else in_dir = opt$i
pos.file = paste(in_dir,"/",pos.file,sep="")
neg.file = paste(in_dir,"/",neg.file,sep="")
if (is.na(opt$d)) {
  out_dir = getwd()
} else out_dir = opt$d
if (opt$v) {
  print(paste("positive file:",pos.file))
  print(paste("negative file:",neg.file))
  print(paste("clonotype type:",opt$c))
  print(paste("freq axis scale:",opt$f))
  print(paste("axis label prefix:",opt$l))
  print(paste("output file prefix:",opt$o))
  print(paste("source files directory:",in_dir))
  print(paste("output directory:",out_dir))
  print(paste("enrichment threshold p-val:",opt$t))
  print(paste("verbose:",opt$v))
}

########## read files ##############################
library(data.table)
library(dplyr)
r1<-fread(pos.file)
r2<-fread(neg.file)

########## handle clonotypes & merge ###############
if (opt$c=="cdr3aa"){
  r1s = r1 %>% group_by(cdr3aa,v,j) %>% summarise(count = sum(count),freq = sum(freq))
  r2s = r2 %>% group_by(cdr3aa,v,j) %>% summarise(count = sum(count),freq = sum(freq))
  r = merge(r2s,r1s,by=c("cdr3aa","v","j"),all = T)
} else{
  r1s = r1 %>% group_by(cdr3nt,cdr3aa,v,j) %>% summarise(count = sum(count),freq = sum(freq))
  r2s = r2 %>% group_by(cdr3nt,cdr3aa,v,j) %>% summarise(count = sum(count),freq = sum(freq))
  r = merge(r2s,r1s,by=c("cdr3nt","cdr3aa","v","j"),all = T)
}
min_freq<-min(min(r$freq.y[!is.na(r$freq.y)]),min(r$freq.x[!is.na(r$freq.x)]))
min_freq_floor = floor(log10(min_freq))
min_freq_floor_log10 = 10^min_freq_floor
breaks_log10 = sapply(c(min_freq_floor:0),function(x){10^x})
labels_log10 = c(0,sapply(c((min_freq_floor+1):0),function(x){10^x}))
axis_ticks = c((min_freq_floor+1):-1)
limits_log10 = c(min_freq_floor_log10,1)
print(breaks_log10)
print(labels_log10)

r = r %>% mutate (
    pseudo.count.x = ifelse(is.na(count.x), 0.1, count.x),
    pseudo.count.y = ifelse(is.na(count.y), 0.1, count.y),
    pseudo.freq.x = ifelse(is.na(freq.x), min_freq_floor_log10, freq.x),
    pseudo.freq.y = ifelse(is.na(freq.y), min_freq_floor_log10, freq.y),
    count.x = ifelse(is.na(count.x), 0, count.x),
    count.y = ifelse(is.na(count.y), 0, count.y),
    freq.x = ifelse(is.na(freq.x), 0, freq.x),
    freq.y = ifelse(is.na(freq.y), 0, freq.y)
)

############# fisher test ##########################
sum_neg<-sum(r$count.x)
sum_poz<-sum(r$count.y)

r = r %>% mutate (
    fisher = mapply(function(x,X,y,Y){
      mat<-matrix(c(x,X-x,y,Y-y),nrow=2,dimnames = list(c("clone", "non-clone"),c("pos", "neg")))
      return(fisher.test(mat)$p.value)
    },x=count.x,X=sum_neg,y=count.y,Y=sum_poz)
  )
r = r %>% mutate(fisher.BH = p.adjust(fisher,method = "BH"))

######## prepare for plot and name outfiles ########
# - conditions for colored points
cond<-(r$fisher.BH<opt$t)&(r$count.y>(r$count.x*sum_poz/sum_neg))
cond2<-(r$fisher.BH<opt$t)&(r$count.y<(r$count.x*sum_poz/sum_neg))
r = r %>% mutate(color = as.factor(ifelse(cond,2,ifelse(cond2,3,1))),
             shape = as.factor(ifelse(cond|cond2,2,1)),
             size = as.factor(ifelse(cond,2,1)))
# - prepare where to put pseudo zero (for count axis)
max_count<-max(max(r$count.y),max(r$count.x))
max_log10<-10^ceiling(log10(max_count))
# - names of axis
pos.file.loc = strsplit(pos.file,"/")[[1]] %>% last
pos.neg.loc = strsplit(neg.file,"/")[[1]] %>% last
if (is.na(opt$l)){
  y.lab = pos.file.loc
  x.lab = pos.neg.loc
} else{
  y.lab = paste(opt$l,"+")
  x.lab = paste(opt$l,"flow")
}
# -name of the plot and by the way outfile names
th = as.character(opt$t)
if (is.na(opt$o)) {
  out_name = "dotplot"
  plot_title = paste(pos.file.loc,"\nvs\n",pos.neg.loc,"\n(",opt$c,";",th,")")
} else {
  out_name = opt$o
  plot_title = paste(out_name,"(",opt$c,";",th,")")
}
outfile_pdf = paste(out_dir,"/",out_name,"_",opt$c,"_",th,".pdf",sep="")
outfile_enr = paste(out_dir,"/",out_name,"_",opt$c,"_",th,".enr.txt",sep="")
outfile_enr_vdj = paste(out_dir,"/",out_name,"_",opt$c,"_",th,".enr.vdj.txt",sep="")

############### plot data ##########################
library(ggplot2)
library(scales)
if (opt$f){
  print(head(r))
  p1 = ggplot(r,aes(pseudo.freq.x,pseudo.freq.y,color=color,shape=shape,size=size))+geom_point()+
    scale_x_log10(breaks = breaks_log10,labels = c(0,sprintf('10^%d',as.integer(axis_ticks)),1),limits = limits_log10)+
    scale_y_log10(breaks = breaks_log10,labels =c(0,sprintf('10^%d',as.integer(axis_ticks)),1),limits = limits_log10)+
    xlab(x.lab)+ylab(y.lab)+scale_colour_manual(values = c("black","red","blue"),guide="none")+scale_shape_manual(values = c(1,19),guide="none")+
    scale_size_manual(values = c(1,2),guide="none")+theme_bw()+
    theme(axis.title =  element_text(size=18),axis.text = element_text(size=20),plot.title = element_text(size=18),
          legend.text =  element_text(size=20),legend.title =  element_text(size=20),plot.margin= unit(c(0.5,1,0.5,0.5),"cm"),aspect.ratio = 1)+ggtitle(plot_title)
}else{
  p1 = ggplot(r,aes(pseudo.count.x,pseudo.count.y,color=color,shape=shape,size=size))+geom_point()+
    scale_x_log10(limits=c(0.1,max_log10),labels = number_format(big.mark=""))+scale_y_log10(limits=c(0.1,max_log10),labels = number_format(big.mark=""))+
    xlab(x.lab)+ylab(y.lab)+scale_colour_manual(values = c("black","red","blue"),guide="none")+scale_shape_manual(values = c(1,19),guide="none")+
    scale_size_manual(values = c(1,2),guide="none")+theme_bw()+
    theme(axis.title =  element_text(size=18),axis.text = element_text(size=20),plot.title = element_text(size=18),
          legend.text =  element_text(size=20),legend.title =  element_text(size=20),plot.margin= unit(c(0.5,1,0.5,0.5),"cm"),aspect.ratio = 1)+ggtitle(plot_title)
}
ggsave(filename=outfile_pdf,plot = p1, width=6,height=6)

############# write enr file #######################
if (opt$c=="cdr3aa"){
  res = r %>% filter(cond) %>% select(cdr3aa,v,j,count.y,count.x,freq.y,freq.x,fisher,fisher.BH) %>% arrange(fisher.BH)
} else{
  res = r %>% filter(cond) %>% select(cdr3nt,cdr3aa,v,j,count.y,count.x,freq.y,freq.x,fisher,fisher.BH) %>% arrange(fisher.BH)
}
res$sum_y = sum_poz
res$sum_x = sum_neg
print(res)
fwrite(res,file = outfile_enr,sep="\t",quote = F)

########### write enr vdj file #####################
if (opt$c=="cdr3aa"){
res_enr_vdj = r1 %>% 
  merge(res, by=c("cdr3aa","v","j")) %>%
  select(count,freq,cdr3nt,cdr3aa,v,d,j,VEnd,DStart,DEnd,JStart)
} else{
  res_enr_vdj = r1 %>% 
    merge(res, by=c("cdr3nt","cdr3aa","v","j")) %>%
    select(count,freq,cdr3nt,cdr3aa,v,d,j,VEnd,DStart,DEnd,JStart)
}
fwrite(res_enr_vdj,file = outfile_enr_vdj,sep="\t",quote = F)

####################################################
################# THE WELLS ########################
####################################################

if (!is.na(opt$w)){
  library(tibble)
  wells.data.df<-fread(opt$w,header=F,col.names = c("sample","file"))
  wells.df = mapply(function(x,w){
    x.file = paste(in_dir,"/",x,sep="")
    return(rownames_to_column(fread(x.file) %>% mutate (well = w) %>% 
                                arrange(desc(freq)),var = "rank") %>% 
             mutate(rank = as.numeric(rank)))
  },wells.data.df$file, wells.data.df$sample,SIMPLIFY = F) %>% rbindlist %>% select(rank,count,freq,cdr3nt,cdr3aa,v,j,well)
  
  if (opt$c=="cdr3aa"){
    r = r %>% merge(wells.df, by = c("cdr3aa","v","j"),all.x = T) %>% group_by(cdr3aa,v,j)
  } else{
    r = r %>% merge(wells.df, by = c("cdr3nt","cdr3aa","v","j"),all.x = T) %>% group_by(cdr3nt,cdr3aa,v,j)
  }
  r = r %>% summarise(
    count.x = dplyr::first(count.x),
    count.y = dplyr::first(count.y),
    freq.x = dplyr::first(freq.x),
    freq.y = dplyr::first(freq.y),
    fisher = dplyr::first(fisher),
    fisher.BH = dplyr::first(fisher.BH),
    pseudo.count.x = dplyr::first(pseudo.count.x),
    pseudo.count.y = dplyr::first(pseudo.count.y),
    wells = paste(well,collapse=","),
    well.max.freq = max(freq),
    well.min.rank = min(rank)) %>% ungroup
  
  r = r %>% mutate(wells = ifelse(wells=="NA","no well",wells),
                   well.max.freq = ifelse(is.na(well.max.freq),0,well.max.freq))
  well.levels = (r %>% filter(cond))$wells %>% sort %>% unique
  well.levels = c("",well.levels)
  r = r %>% mutate(color = factor(ifelse(cond,wells,""),levels = well.levels),
                   shape = as.factor(ifelse(cond,2,1)),
                   size = ifelse(cond,well.max.freq,0))
  
  # if more than 18 - will be error!!!
  cbbPalette <- c("#000000","#000000", "#E41A1C" ,"#377EB8", "#4DAF4A" ,"#984EA3", "#FF7F00" ,"#FFFF33", "#A65628" ,"#F781BF",
                  "#8DD3C7" ,"#FFFFB3" ,"#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5")
  
  used_colors_1 = as.numeric(r$color) %>% sort %>% unique
  print(r[cond,c("pseudo.count.x","pseudo.count.y","color","shape","size","wells")])
  if (opt$f){
    p1 = ggplot(r,aes(pseudo.freq.x,pseudo.freq.y,color=color,shape=shape,size=size))+geom_point()+
      scale_x_log10(breaks = breaks_log10,labels = c(0,sprintf('10^%d',as.integer(axis_ticks)),1),limits = limits_log10)+
      scale_y_log10(breaks = breaks_log10,labels = c(0,sprintf('10^%d',as.integer(axis_ticks)),1),limits = limits_log10)+
      xlab(x.lab)+ylab(y.lab)+scale_shape_manual(values = c(1,19),guide="none")+
      scale_size_continuous(guide="none")+scale_color_manual(values = cbbPalette[used_colors_1])+
      theme_bw()+
      theme(axis.title =  element_text(size=18),axis.text = element_text(size=20),plot.title = element_text(size=18),
            legend.text =  element_text(size=20),legend.title =  element_text(size=20),plot.margin= unit(c(0.5,1,0.5,0.5),"cm"), aspect.ratio = 1)+ggtitle(plot_title)
  }else{
    p1 = ggplot(r,aes(pseudo.count.x,pseudo.count.y,color=color,shape=shape,size=size))+geom_point()+
      scale_x_log10(limits=c(0.1,max_log10),labels = number_format(big.mark=""))+scale_y_log10(limits=c(0.1,max_log10),labels = number_format(big.mark=""))+
      xlab(x.lab)+ylab(y.lab)+scale_shape_manual(values = c(1,19),guide="none")+
      scale_size_continuous(guide="none")+scale_color_manual(values = cbbPalette[used_colors_1])+
      theme_bw()+
      theme(axis.title =  element_text(size=18),axis.text = element_text(size=20),plot.title = element_text(size=18),
            legend.text =  element_text(size=20),legend.title =  element_text(size=20),plot.margin= unit(c(0.5,1,0.5,0.5),"cm"),aspect.ratio = 1)+ggtitle(plot_title)
  }
  
  # get top 20 from each well
  wells.top.20 = wells.df %>% 
    group_by(well) %>%
    top_n(20,freq)

  if (opt$c=="cdr3aa"){
    res.w = r %>% filter(cond) %>% select(cdr3aa,v,j,count.y,count.x,freq.y,freq.x,fisher,fisher.BH,wells) %>% arrange(fisher.BH)
    wells.top.20 = wells.top.20 %>% merge(res.w,by = c("cdr3aa","v","j"),all.x = T)
  } else{
    res.w = r %>% filter(cond) %>% select(cdr3nt,cdr3aa,v,j,count.y,count.x,freq.y,freq.x,fisher,fisher.BH,wells) %>% arrange(fisher.BH)
    wells.top.20 = wells.top.20 %>% merge(res.w,by = c("cdr3nt","cdr3aa","v","j"),all.x = T)
  }
  wells.top.20 = wells.top.20 %>% mutate(wells = factor(ifelse(is.na(wells),"no well",wells),levels = well.levels))

  used_colors_2 = as.numeric(wells.top.20$wells) %>% sort %>% unique
  p2 = ggplot(wells.top.20)+geom_col(aes(x=rank,y=freq,group=well,fill=wells),position="dodge")+
    facet_wrap(~well,ncol = 2)+theme_bw()+scale_fill_manual(values = cbbPalette[used_colors_2],guide="none")+
    theme(axis.title =  element_text(size=20),axis.text = element_text(size=20))
  library(gridExtra)
  p3 = grid.arrange(p1,p2,widths=c(2.5/4, 1.5/4),nrow=1)
  
  outfile_w_pdf = paste(out_dir,"/",out_name,"_",opt$c,"_",th,"_wells.pdf",sep="")
  ggsave(filename=outfile_w_pdf, plot = p3, width=12,height=6)
  
  res.w$sum_y = sum_poz
  res.w$sum_x = sum_neg
  print(res.w)
  outfile_enr_w = paste(out_dir,"/",out_name,"_",opt$c,"_",th,"_wells.enr.txt",sep="")
  
  fwrite(res.w,file = outfile_enr_w,sep="\t",quote = F)
}
