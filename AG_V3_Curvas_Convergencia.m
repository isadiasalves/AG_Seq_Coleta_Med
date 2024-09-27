clc
clear all
close all

Dados_10 = csvread('dist_converg_V3_10.csv',0,0);

Cromossomos_10 = Dados_10(:,1);
Distancias_10 = Dados_10(:,2);

figure (1)
plot(Cromossomos_10, Distancias_10, 'LineWidth', 0.9)
xlim([1 20]);
ylim([45 50]);
xticks(2:2:20);
yticks(45:1:50);
xlabel('Geração', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k')
ylabel('Distância', 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k')