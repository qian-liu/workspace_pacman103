clear
%dirStr = ['0/'; '1/'; '2/'; '5/'; 't/'];
dirStr = ['11/'; '12/'; '13/'; '14/'; '15/'; '16/'];
rate_array = [];
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, 200, 10000 );
        temp_array = [temp_array; rate'];
    end
    rate_array = [rate_array temp_array];
end

hold all
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    temp = temp/max(temp);
    plot( temp );
end
xlabel('Time in ms')
ylabel('Spikes rates');
set(gca,'Xlim',[0,300],'XTick',[0:30:300] ,'XTicklabel',0:30*200:300*200);