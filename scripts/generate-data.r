# Read data from .csv file
data <- read.table("table.csv", header=TRUE, sep=";")
#data <- read.table("table-outliers.csv", header=TRUE, sep=";")

# Histograms
png("./graphics/hist-nofi.png")
hist(data$NoFi)
dev.off()

png("./graphics/hist-nom.png")
hist(data$NoM)
dev.off()

png("./graphics/hist-mwde.png")
hist(data$MwDe)
dev.off()

png("./graphics/hist-sloc.png")
hist(data$SLoC)
dev.off()

png("./graphics/hist-node.png")
hist(data$NoDe)
dev.off()



# Answering the first question
# Correlations between NoFi/NoM/SLoC and NoDe
cor_nofi <- cor(data$NoFi, data$NoDe, method="kendall")
cor_nofi
cor_nom <- cor(data$NoM, data$NoDe, method="kendall")
cor_nom
cor_mwde <- cor(data$MwDe, data$NoDe, method="kendall")
cor_mwde
cor_sloc <- cor(data$SLoC, data$NoDe, method="kendall")
cor_sloc
cor_nom_sloc <- cor(data$NoM, data$SLoC, method="kendall")
cor_nom_sloc

# Plots
node_ymarks <- c(10, 100, 1000, 10000, 80000)
node_ylabels=c("10", "100", "1K", "10K", "80K")

# NoFi / NoDe
png("./graphics/nofi-node.png", width=300, height=300)
xmarks <- c(20, 100, 500, 3000, 15000)
xlabels <- c("20", "100", "500", "3K", "15K")
plot(data$NoFi, data$NoDe, type="p", xlab="NoFi", ylab="NoDe", log="xy", xaxt="n", yaxt="n")
axis(1, at=xmarks, labels=xlabels)
axis(2, at=node_ymarks, labels=node_ylabels)
dev.off()

# NoM/NoDe
png("./graphics/nom-node.png", width=300, height=300)
xmarks <- c(500, 3000, 30000, 200000)
xlabels <- c("500", "3K", "30K", "200K")
plot(data$NoM, data$NoDe, type="p", xlab="NoM", ylab="NoDe", log="xy", xaxt="n", yaxt="n")
axis(1, at=xmarks, labels=xlabels)
axis(2, at=node_ymarks, labels=node_ylabels)
dev.off()

# MwDe / NoDe
png("./graphics/mwde-node.png", width=300, height=300)
xmarks <- c(5, 50, 200, 1000, 10000)
xlabels <- c("5", "50", "200", "1K", "10K")
plot(data$MwDe, data$NoDe, type="p", xlab="MwDe", ylab="NoDe", log="xy", xaxt="n", yaxt="n")
axis(1, at=xmarks, labels=xlabels)
axis(2, at=node_ymarks, labels=node_ylabels)
dev.off()

# SLoC / NoDe
png("./graphics/sloc-node.png", width=300, height=300)
xmarks <- c(100, 1000, 10000, 100000, 1000000, 9000000)
xlabels=c("100", "1k", "10k", "100K", "1M", "9M")
plot(data$SLoC, data$NoDe, type="p", xlab="SLoC", ylab="NoDe", log="xy", xaxt="n", yaxt="n")
axis(1, at=xmarks, labels=xlabels)
axis(2, at=node_ymarks, labels=node_ylabels)
dev.off()

nom_nofi = data$NoM/data$NoFi
mean_nom_nofi = mean(nom_nofi)
mean_nom_nofi
sd_nom_nofi = sd(nom_nofi)
sd_nom_nofi



# Answering the second question
debug = data$X.debug/data$NoDe
elif = data$X.elif/data$NoDe
elifdef = data$X.elifdef/data$NoDe
elifndef = data$X.elifndef/data$NoDe
xelse = data$X.else/data$NoDe
xif = data$X.if/data$NoDe
ifdef = data$X.ifdef/data$NoDe
ifndef = data$X.ifndef/data$NoDe
mdebug = data$X.mdebug/data$NoDe

mean(elif)
sd(elif)
mean(xelse)
sd(xelse)
mean(xif)
sd(xif)
mean(ifdef)
sd(ifdef)
mean(ifndef)
sd(ifndef)


# Answering the third question
# Correlation between NoFe and NoDe
cor_nofe <- cor(data$NoFE, data$NoDe, method="kendall")
cor_nofe
cor_nom_nofe <- cor(data$NoM, data$NoFE, method="kendall")
cor_nom_nofe

# Plots
png("./graphics/nofe-node.png", width=300, height=300)
xmarks <- c(10, 100, 1000, 10000)
xlabels=c("10", "100", "1k", "10k")
plot(data$NoFE, data$NoDe, type="p", xlab="NoFe", ylab="NoDe", log="xy", xaxt="n", yaxt="n")
axis(1, at=xmarks, labels=xlabels)
axis(2, at=node_ymarks, labels=node_ylabels)
dev.off()

png("./graphics/nom-nofe.png", width=300, height=300)
plot(data$NoM, data$NoFE, type="p", xlab="NoM", ylab="NoFe")
dev.off()
