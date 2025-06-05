% using documentation found at https://www.mathworks.com/help/signal/ref/ellipord.html

%%%%%%%%%%%%%%%%%%% Part (a) - Lowpass Filter %%%%%%%%%%%%%%%%%%%
figure;
% given values for lowpass filter
Wp = 0.2;
Ws = 0.3;
Rp = 1;
As = 15;

[n, Wn] = ellipord(Wp, Ws, Rp, As);
[b, a] = ellip(n, Rp, As, Wn, 'low');

% frequency response using freqz
freqz(b, a);
title('Lowpass Elliptic Filter');

%%%%%%%%%%%%%%%%%%% Part (b) - Highpass Filter %%%%%%%%%%%%%%%%%%%
figure;
% given values for highpass filter
Wp = 0.6;
Ws = 0.4;
Rp = 1;
As = 15;

[n, Wn] = ellipord(Wp, Ws, Rp, As);
[b, a] = ellip(n, Rp, As, Wn, 'high');

% frequency response using freqz
freqz(b, a);
title('Highpass Elliptic Filter');

%%%%%%%%%%%%%%%%%%% Part (c) - Bandpass Filter %%%%%%%%%%%%%%%%%%%
figure;
% given values for bandpass filter
Wp = [0.4, 0.6];
Ws = [0.3, 0.75];
Rp = 1;
As = 40;

[n, Wn] = ellipord(Wp, Ws, Rp, As);
[b, a] = ellip(n, Rp, As, Wn, 'bandpass');

% frequency response using freqz
freqz(b, a);
title('Bandpass Elliptic Filter');

%%%%%%%%%%%%%%%%%%% Part (d) - Bandstop Filter %%%%%%%%%%%%%%%%%%%
figure;
% given values for bandstop filter
Wp = [0.25, 0.8];
Ws = [0.4, 0.7];
Rp = 1;
As = 40;

[n, Wn] = ellipord(Wp, Ws, Rp, As);
[b, a] = ellip(n, Rp, As, Wn, 'stop');

% frequency response using freqz
freqz(b, a);
title('Bandstop Elliptic Filter');
