

library(survival)
library(survminer)
library(ggplot2)
library(survival)
library(esquisse)

survival::ovarian
head(ovarian, 20)

T=1:1200


df<-Surv(ovarian$futime, ovarian$fustat)
df

Visual<-survfit(Surv(futime,fustat)~1, data=ovarian)

plot(Visual, main="Ovarian Survival")

Model<-survreg(df~1, dist='weibull',scale=0 )
summary(Model)
# Model$coefficients is intercept,   Model$scale is scale
# gamma = 1/scale.   alpha= exp(intercept)

gamma = 1/Model$scale
alpha= exp(Model$coefficients)

plot(Visual, main="Ovarian Survival")
lines(T, 1-pweibull(T,shape=gamma, scale=alpha))


