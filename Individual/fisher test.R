
set.seed(5318008)

bryce_fisher <-
  function(p_vals = runif(100)){
  log_p_vals <- log(p_vals)
  T_val <- -2* sum(log_p_vals)
  freedom_degs <- length(p_vals)*2
  
  fish <- pchisq(q = T_val, df = freedom_degs, lower.tail = FALSE)
  
  return(fish)
  }

alpha_perc <- function(p_vals, alpha = 0.05){
  sum(p_vals < alpha)/length(p_vals)
}

nums_gen <- 10^(1:4)

for (i in 1:length(nums_gen)){
  a <- replicate(10000, bryce_fisher(runif(nums_gen[i])))
  assign(paste0('test_', nums_gen[i]), a)
  print(alpha_perc(a))
  plot(ecdf(a), main = paste0('ECDF for fishers n =', nums_gen[i]))
  # not very efficient here, wanted to assign the Ps produced but also wanted to do some stuff with em
  # definitely better method exists
  rm(a)
}
