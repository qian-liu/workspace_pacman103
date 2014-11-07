hold all;
for i = 0:4
    file_name = sprintf('14/recog_%d.spikes',i);
    rate = showRate( file_name, 210, 10000, 16 );
    %temp_array = [temp_array; rate'];
    plot(rate);
    %plot(rate/max(rate));
end