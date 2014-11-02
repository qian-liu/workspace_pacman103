hold all
for i = 0:4
    file_name = sprintf('recog_%d.spikes', i);
    rate = showRate( file_name );
    plot(rate);
end
hold off