%% Data
% Full Size Range
size = [ 5 10 20 40 80 160 320 640 1280 2560 5120 10240 ];

% Basic Color Refinement
% Measurement 1
sizeb1 = [ 5 10 20 40 80 160 320 640 1280 2560 5120 ];
timeb1 = [ 0.000447894 0.001738771 0.007223303 0.031326249 0.125898654 0.604074251 3.213163267 19.26075537 127.5672593 907.4070568 5736.549588 ];
% Slides w/out adjacency
sizeb2 = [ 160 320 640 ];
timeb2 = [ 7 54 427 ];
% Slides w/ adjacency
sizeb3 = [ 160 320 640 1280 ];
timeb3 = [ 0.3 2 17 125 ];

% Fast Color Refinement
% Measurement 1
sizef1 = [ 5 10 20 40 80 160 320 640 1280 2560 5120 10240 20480];
timef1 = [ 0.00058746337890625 0.0008630752563476562 0.0017960071563720703 0.0044100284576416016 0.007059335708618164 0.014141559600830078 0.028933286666870117 0.058183908462524414 0.11742138862609863 0.26059627532958984 0.491408348083496 0.994426965713501 2.088636636734009 ];
% Slides w/ adjacency
sizef2 = [ 160 320 640 1280 2560 5120 10240 ];
timef2 = [ 0.04 0.09 0.13 0.3 1 3 12 ];
% Measurement 2
sizef3 = size;
timef3 = [ 0.000124264999612933 0.000342142000590683 0.00100838100024702 0.00321382000038283 0.0112542269998812 0.0411697640001875 0.157870802999241 0.60982414099999 2.40300816400031 9.60912720700071 42.0685733139998 188.312010114 ];


%% Basic Computation Time Subplot

%subplot(2,1,1);

% Basic Measurement 1
p = semilogy(sizeb1, timeb1);
p.Color = 'blue';
p.Marker = '.';
p.MarkerSize = 10;
p.LineWidth = 1;

hold on
title('Computation Time of Basic Color Refinement for Threepaths');
xlabel('Size \it (# vertices per path)');
ylabel('Time \it (s)');
xlim([5 5120]);
xlabels = [ 5 640 1280 2560 5120 10240 ];
set(gca, 'Xtick', xlabels);
set(gca, 'XtickLabel', xlabels);

% x^2
x = 0:5:10240;
p = semilogy(x, x.^2);
p.Color = 'black';

% x^3
p = semilogy(x, x.^3);
p.Color = 'red';

legend('color refinement', 'n^2', 'n^3');
legend('Location','southeast');
legend('boxon');

%% Fast Computation Time Subplot

%subplot(2,1,1);

% Basic Measurement 1
p = semilogy(sizef1, timef1);
p.Color = 'blue';
p.Marker = '.';
p.MarkerSize = 10;
p.LineWidth = 1;

hold on
title('Computation Time of Fast Color Refinement for Threepaths');
xlabel('Size \it (# vertices per path)');
ylabel('Time \it (s)');
xlim([5 20480]);
xlabels = [ 5 2560 5120 10240  20480];
set(gca, 'Xtick', xlabels);
set(gca, 'XtickLabel', xlabels);

% log2n
x = 0:5:20480;
p = semilogy(x, log2(x));
p.Color = 'black';

% nlog2n
x = 0:5:20480;
p = semilogy(x, x.*log2(x));
p.Color = 'red';

legend('color refinement', 'log_2n', 'n\cdotlog_2n');
legend('Location','southeast');
legend('boxon');

%% Other plots
% Basic Slides w/out Adjacency
p = semilogy(sizeb2, timeb2);
p.Color = 'magenta';
p.Marker = 'o';
p.MarkerSize = 6;

% Basic Slides w/ Adjacency
p = semilogy(sizeb3, timeb3);
p.Color = 'green';
p.Marker = 'o';
p.MarkerSize = 6;

% Fast Slides w/ Adjacency
p = semilogy(sizef2, timef2);
p.Color = 'cyan';
p.Marker = 'o';
p.MarkerSize = 6;

% x^2
x = 0:5:10240;
p = semilogy(x, x.^2);
p.Color = 'red';

% x^3
p = semilogy(x, x.^3);
p.Color = 'black';

legend('Measurements', 'Slides w/out adjacency', 'Slides w/ adjacency', 'Fast slides w/ adjacency', 'Quadratic', 'Qubic', 'Location', 'northwest', 'Orientation', 'vertical');
%legend();
%legend();
%legend('boxon');

%% Relative Growth Basic Subplot
m2 = sizeb1.^2;
diff2 = m2./timeb1;
m3 = sizeb1.^3;
diff3 = m3./timeb1;
diff = [ diff3.' diff2.' ];

%subplot(2,1,2);
figure

bar_handle = bar(diff, 'grouped');
set(gca, 'YScale', 'log');
set(bar_handle(1), 'FaceColor', 'red')
set(bar_handle(2), 'FaceColor', 'black')

set(gca, 'XtickLabel', sizeb1);

title('Relative Differences between Basic Algorithm and Functions')
xlabel('Size \it (# vertices per path)')
ylabel('Function divided by computation time')

legend('n^3', 'n^2');
legend('Location','northwest');
legend('boxon');

%% Relative Growth Fast Subplot
m4 = sizef1.*log2(sizef1);
diff4 = m4./timef1;
m5 = sizef1.^2;
diff5 = m5./timef1;
m6 = sizef1.^3;
diff6 = m6./timef1;
m7 = sizef1.^2.*log2(sizef1);
diff7 = m7./timef1;
m8 = log(sizef1);
diff8 = m8./timef1;
diff = [ diff4.' diff8.'];

%subplot(2,1,2);
figure

bar_handle = bar(diff, 'grouped');
set(gca, 'YScale', 'log');
set(bar_handle(1), 'FaceColor', 'red')
set(bar_handle(2), 'FaceColor', 'black')
%set(bar_handle(3), 'FaceColor', 'yellow')
%set(bar_handle(4), 'FaceColor', 'cyan')
%set(bar_handle(5), 'FaceColor', 'green')

xticks = [ 1 2 3 4 5 6 7 8 9 10 11 12 13 ];
xlabels = [ 5 10 20 40 80 160 320 640 1280 2560 5120 10240 20480 ];
set(gca, 'Xtick', xticks);
set(gca, 'XtickLabel', xlabels);
set(gca, 'XtickLabelRotation', 30);

title('Relative Differences between Fast Algorithm and Functions')
xlabel('Size \it (# vertices per path)')
ylabel('Function divided by computation time')

legend('n\cdotlog_2n', 'log_2n');
legend('Location','northwest');
legend('boxon');
