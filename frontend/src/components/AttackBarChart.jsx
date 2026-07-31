import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from 'recharts';
import '../styles/Charts.css';

const BAR_COLORS = [
  '#ef4444', '#f59e0b', '#3b82f6', '#06b6d4', 
  '#a855f7', '#ec4899', '#10b981', '#6366f1'
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-chart-tooltip">
        <p className="tooltip-label">{label}</p>
        <p className="tooltip-value">{new Intl.NumberFormat().format(payload[0].value)} occurrences</p>
      </div>
    );
  }
  return null;
};

const AttackBarChart = ({ attack_breakdown = {} }) => {
  const data = Object.keys(attack_breakdown).map((key) => ({
    category: key,
    count: attack_breakdown[key]
  })).sort((a, b) => b.count - a.count);

  return (
    <div className="glass-card chart-card">
      <div className="chart-header">
        <h3 className="chart-title">Attack Category Breakdown</h3>
        <span className="chart-subtitle">Multi-class threat categorization</span>
      </div>
      <div style={{ flex: 1, width: '100%', minHeight: 0 }}>
        {data.length === 0 ? (
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#64748b' }}>
            No attack traffic detected
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
              <XAxis 
                dataKey="category" 
                stroke="#64748b" 
                fontSize={11} 
                tickLine={false} 
                interval={0}
                angle={-25}
                textAnchor="end"
              />
              <YAxis stroke="#64748b" fontSize={11} tickLine={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {data.map((entry, index) => (
                  <Cell key={`bar-${index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

export default AttackBarChart;
