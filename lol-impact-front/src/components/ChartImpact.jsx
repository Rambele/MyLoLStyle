import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  LabelList,
} from 'recharts';

const colorMap = {
  damageDealtToBuildings: '#ef4444',
  totalDamageDealt: '#3b82f6',
  totalDamageTaken: '#f97316',
  healing_done: '#a855f7',
  goldEarned: '#10b981',
  killParticipation: '#eab308',
  // Ajoute d'autres mappings...
};

const ChartImpact = ({ data }) => {
  const barWidth = 120;
  const chartWidth = Math.max(600, data.length * barWidth); // largeur min = 600px

  return (
    <div className="overflow-x-auto">
      <div style={{ width: chartWidth, height: 500 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 20, right: 30, bottom: 60, left: 20 }}
          >
            <XAxis dataKey="stat" type="category" interval={0} angle={-45} textAnchor="end" />
            <YAxis type="number" />
            <Tooltip formatter={(val) => val.toFixed(2)} />
            <Bar dataKey="value">
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colorMap[entry.stat] || '#38bdf8'} />
              ))}
              <LabelList
                dataKey="value"
                position="top"
                fill="white"
                formatter={(val) => val.toFixed(2)}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartImpact;
