function [ output_rate ] = showRate( file_name, frame_len, run_time )
%SHOWRATE Summary of this function goes here
%   Detailed explanation goes here
    %frame_len = 30;
    %integrate = load( file_name );
    fid = fopen( file_name );
    for i = 1:4
        fgetl(fid);
    end
    temp = textscan(fid, '%f %f', 'CollectOutput', 1);
    integrate = temp{1,1};
    integrate = sortrows( integrate, 1 );
    frame_num = 0;
    rsize = 16;
    r_image = zeros(rsize, rsize);
    output_rate = [];
    for i = 1 : size(integrate, 1)
        if ceil( (integrate(i,1) + 1) /frame_len) > frame_num
            r_image = flipud(r_image);
            %imagesc(r_image);
            spike_count = sum(sum(r_image));
            output_rate = [output_rate; spike_count];
            for j = 1 : ceil( (integrate(i,1) + 1) /frame_len) - frame_num -1
                output_rate = [output_rate; 0];
            end
            %pause(0.1);
            r_image = zeros(rsize, rsize);
            frame_num = ceil( (integrate(i,1) + 1) /frame_len) ;
        else
            neuron_id = integrate(i, 2);
            index_y = floor(neuron_id / rsize) + 1;
            index_x = mod(neuron_id, rsize) + 1;
            r_image(index_x,index_y) = r_image(index_x,index_y) + 1;
        end
    end
    len_rate = length(output_rate);
    if len_rate < run_time/frame_len
        len_temp = floor(run_time/frame_len) - len_rate;
        temp = zeros(len_temp, 1);
        output_rate = [output_rate; temp];
    end
    fclose(fid);
end

