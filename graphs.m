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

% Slides w/ adjacency
sizef2 = [ 160 320 640 1280 2560 5120 10240 ];
timef2 = [ 0.04 0.09 0.13 0.3 1 3 12 ];

%% Computation Time Subplot

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

%%
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

%% Relative Growth Subplot
m2 = sizeb1.^2;
diff2 = m2./timeb1;
m3 = sizeb1.^3;
diff3 = m3./timeb1;
diff = [ diff2.' diff3.'];

%subplot(2,1,2);
figure

bar_handle = bar(diff, 'grouped');
set(gca, 'YScale', 'log');
set(bar_handle(1), 'FaceColor', 'red')
set(bar_handle(2), 'FaceColor', 'black')

set(gca, 'XtickLabel', sizeb1);

title('Relative Differences between Measurements and (x^2 and x^3)')
xlabel('Size \it (# vertices per path)')
ylabel('x^2 and x^3 divided by Measurements')

legend('Diff w/ quadratic', 'Diff w/ cubic');
legend('Location','northwest');
legend('boxon');