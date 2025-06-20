import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, LabelList } from 'recharts';

const colorMap = {
  damage_to_champs: '#ef4444',
  damage_to_turrets: '#facc15',
  ward_control: '#22c55e',
  objective_impact: '#3b82f6',
  healing_done: '#a855f7',
  damage_taken: '#f97316',
  gold_contribution: '#10b981',
  kda_ratio: '#eab308',
  // Ajoute plus de couleurs ici...
};

const ChartImpact = ({ data }) => {
  const barCount = data.length;
  const minHeight = 300;
  const dynamicHeight = Math.max(minHeight, barCount * 60); // 60px par stat minimum

  return (
    <ResponsiveContainer width="100%" height={dynamicHeight}>
      <BarChart data={data} margin={{ bottom: 60 }}>
        <XAxis dataKey="stat" type="category" />
        <YAxis type="number" />
        <Tooltip />
        <Bar dataKey="value">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={colorMap[entry.stat] || '#38bdf8'} />
          ))}
          <LabelList dataKey="value" position="top" fill="white" />
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};


export default ChartImpact;
