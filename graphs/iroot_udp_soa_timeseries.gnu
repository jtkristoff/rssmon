set terminal postscript eps enhanced color font 'Helvetica,22'
set output 'iroot_udp_soa_timeseries.eps'
##
##
set datafile missing '-'
set style data points
set size 1.2,1
set xtics border in scale 1,0.5 nomirror offset character 0, 0, 0 autojustify
set xtics  norangelimit
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set format x "%m/%d"
set format y "%4.3f"
set grid ytics lc rgb "#C0C0C0"
set grid xtics lc rgb "#C0C0C0"
set xtics font ", 18"
set ytics font ", 18"
set ylabel "RTT"
set ylabel offset 2.2
set xlabel "timestamp"
set yrange [-15:500]
set xrange ["2019-05-11" : "2019-05-12"]


grid_color = "#d5e0c9"
set key top right
plot 'iroot_udp_soa_timeseries.dat' using 1:2 pt 6 ps 1 lt rgb "black" notitle
