hold all;
for i = 0:4
    file_name = sprintf('14/recog_%d.spikes',i);
    rate = showRate( file_name, 200, 10000 );
    %temp_array = [temp_array; rate'];
    plot(rate);
    %plot(rate/max(rate));
end