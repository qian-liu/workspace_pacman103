clear
%dirStr = ['0/'; '1/'; '2/'; '5/'; 't/'];
dirStr = ['11/'; '12/'; '13/'; '14/'; '15/'; '16/'];
rate_array = [];
threashold = [0.2, 0.2, 0.2, 0.2, 0.2];
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, 300, 10000 );
        temp_array = [temp_array; rate'];
    end
    rate_array = [rate_array temp_array];
end

hold all
rate_array_normal = zeros(size(rate_array));
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    temp = temp/max(temp);
    plot( temp );
    temp(temp < threashold(iDir)) = 0;
    rate_array_normal(iDir, :) = temp;
end
xlabel('Time in ms')
ylabel('Spikes rates');
set(gca,'Xlim',[0,200],'XTick',[0:20:200] ,'XTicklabel',0:20*300:200*300);

gin=[1+5, 41+5, 81+5, 136+5, 166+5, 205];
frame_num = zeros(1,5);
reject = zeros(1,5);
correct = zeros(1,5);
wrong = zeros(1,5);
for i = 1 : 5
    rate_array_normal(iDir, :);
    temp = rate_array_normal(:, gin(i):gin(i+1)-1);
    [max_t, index_t] = max(temp);
    frame_num(i) = gin(i+1) - gin(i);
    reject(i) = size(find(max_t == 0), 2);
    correct(i) = size(find(index_t(max_t > 0) == i),2);
    wrong(i) = frame_num(i) - reject(i) - correct(i);
end