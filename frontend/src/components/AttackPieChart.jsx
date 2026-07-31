import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import '../styles/Charts.css';

const COLORS = ['#22c55e', '#ef4444'];

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0];
    return (
      <div className="custom-chart-tooltip">
        <p className="tooltip-label">{data.name}</p>
        <p className="tooltip-value">{new Intl.NumberFormat().format(data.value)} packets</p>
      </div>
    );
  }
  return null;
};

const AttackPieChart = ({ normal_count = 0, attack_count = 0 }) => {
  const data = [
    { name: 'Normal Traffic', value: normal_count },
    { name: 'Attacks Detected', value: attack_count }
  ];

  return (
    <div className="glass-card chart-card">
      <div className="chart-header">
        <h3 className="chart-title">Normal vs Attack Proportion</h3>
        <span className="chart-subtitle">Binary classification breakdown</span>
      </div>
      <div style={{ flex: 1, width: '100%', minHeight: 0 }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={95}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend verticalAlign="bottom" height={36} iconType="circle" />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AttackPieChart;
