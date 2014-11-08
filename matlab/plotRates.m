clear
%dirStr = ['0/'; '1/'; '2/'; '5/'; 't/'];
%dirStr = ['11/'; '12/'; '13/'; '14/'; '15/'; '16/'];
%dirStr = ['01/'; '02/'; '03/'; '04/'; '05/'; '06/'];
%dirStr = ['32_ 1/'; '32_ 2/'; '32_ 3/'; '32_ 4/'; '32_ 5/'; '32_ 6/'; '32_ 7/'; '32_ 8/'; '32_ 9/'; '32_10/'; '32_11/'; '32_12/'];
%-----------------------plot 1---------------------------------------%
dirStr = ['128/'];
rate_array = [];
%threashold = [0.2, 0.2, 0.2, 0.2, 0.2]*1.5;
%threashold = [6.5, 5.5, 5.5, 5.5, 5.5];
threashold = 2.5 *ones(1,5);
rsize = 16;
frame_len =30;
run_time = 66000;
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, frame_len, run_time, rsize );
        temp_array = [temp_array; rate'];
    end
    rate_array = [rate_array temp_array];
end
%rate_array(3,70) = 50;
%rate_array(4,70) =100;
subplot(4,1,1);
hold all
rate_array_normal = zeros(size(rate_array));
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    %temp = temp/max(temp);
    plot( temp );
    temp(temp < threashold(iDir)) = 0;
    rate_array_normal(iDir, :) = temp;
end
xlabel('Time in ms')
ylabel('Spikes rates');
plot_time = 60000;
set(gca,'Xlim',[0,plot_time/frame_len],'Ylim',[0,20],'XTick',[0:plot_time/frame_len/10:plot_time/frame_len] ,'XTicklabel',0:plot_time/10:plot_time);
title('128 * 128 Input. Spike rates per 30ms.');

%gin=[1+5, 41+5, 81+5, 136+5, 166+5, 205];
gin=[1, 425, 825, 1385, 1697, 2050];
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
frame_num
reject./frame_num
correct./(correct + wrong)

%-----------------------plot 2---------------------------------------%

threashold = 10.5 *ones(1,5);
rsize = 16;
frame_len =300;
run_time = 66000;
rate_array=[]
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, frame_len, run_time, rsize );
        temp_array = [temp_array; rate'];
    end
    rate_array = [rate_array temp_array];
end
%rate_array(3,70) = 50;
%rate_array(4,70) =100;
subplot(4,1,2);
hold all
rate_array_normal = zeros(size(rate_array));
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    %temp = temp/max(temp);
    plot( temp );
    temp(temp < threashold(iDir)) = 0;
    rate_array_normal(iDir, :) = temp;
end
xlabel('Time in ms')
ylabel('Spikes rates');
plot_time = 60000;
set(gca,'Xlim',[0,plot_time/frame_len],'Ylim',[0,100],'XTick',[0:plot_time/frame_len/10:plot_time/frame_len] ,'XTicklabel',0:plot_time/10:plot_time);
title('128 * 128 Input. Spike rates per 300ms.');

%gin=[1+5, 41+5, 81+5, 136+5, 166+5, 205];
gin=[1, 42, 82, 138, 169, 205];
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
frame_num
reject./frame_num
correct./(correct + wrong)
threashold = 2.5 *ones(1,5);

dirStr = ['321/';'322/'];

%threashold = [0.2, 0.2, 0.2, 0.2, 0.2]*1.5;
%threashold = [6.5, 5.5, 5.5, 5.5, 5.5];
threashold = 3.5 *ones(1,5);
rsize = 14;
frame_len =30;
run_time = 66000;
rate_array = zeros(5,run_time/frame_len +1);
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, frame_len, run_time, rsize );
        temp_array = [temp_array; rate'];
    end
    rate_array = rate_array + temp_array;
end
%rate_array(3,70) = 50;
%rate_array(4,70) =100;
subplot(4,1,3);
hold all
rate_array_normal = zeros(size(rate_array));
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    %temp = temp/max(temp);
    plot( temp );
    temp(temp < threashold(iDir)) = 0;
    rate_array_normal(iDir, :) = temp;
end
xlabel('Time in ms')
ylabel('Spikes rates');
plot_time = 60000;
set(gca,'Xlim',[0,plot_time/frame_len],'Ylim',[0,20],'XTick',[0:plot_time/frame_len/10:plot_time/frame_len] ,'XTicklabel',0:plot_time/10:plot_time);
title('32 * 32 Input. Spike rates per 30ms.');

gin=[1, 425, 825, 1385, 1697, 2050];
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
frame_num
reject./frame_num
correct./(correct + wrong)


threashold = 15.5 *ones(1,5);
rsize = 14;
frame_len =300;
run_time = 66000;
rate_array = zeros(5,run_time/frame_len +1);
for iDir = 1 : size(dirStr,1)
    temp_array = [];
    for i = 0:4
        file_name = sprintf('%srecog_%d.spikes', dirStr(iDir, :),i);
        rate = showRate( file_name, frame_len, run_time, rsize );
        temp_array = [temp_array; rate'];
    end
    rate_array = rate_array + temp_array;
end
%rate_array(3,70) = 50;
%rate_array(4,70) =100;
subplot(4,1,4);
hold all
rate_array_normal = zeros(size(rate_array));
for iDir = 1 : 5
    temp = rate_array(iDir, :);
    %temp = temp/max(temp);
    plot( temp );
    temp(temp < threashold(iDir)) = 0;
    rate_array_normal(iDir, :) = temp;
end
xlabel('Time in ms')
ylabel('Spikes rates');
plot_time = 60000;
set(gca,'Xlim',[0,plot_time/frame_len],'Ylim',[0,100],'XTick',[0:plot_time/frame_len/10:plot_time/frame_len] ,'XTicklabel',0:plot_time/10:plot_time);
title('128 * 128 Input. Spike rates per 300ms.');

gin=[1, 42, 82, 138, 169, 205];
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
frame_num
reject./frame_num
correct./(correct + wrong)