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

const STAT_LABELS = {
  controlWardsPlaced: "Balises de contrôle posées",
  damageDealtToBuildings: "Dégâts aux bâtiments",
  damageDealtToObjectives: "Dégâts aux objectifs",
  damageDealtToTurrets: "Dégâts aux tourelles",
  damageSelfMitigated: "Dégâts auto-mitigés",
  deaths: "Morts",
  effectiveHealAndShielding: "Soins et boucliers effectifs",
  enemyChampionImmobilizations: "Immobilisations d'ennemis",
  goldEarned: "Or gagné",
  immobilizeAndKillWithAlly: "Immobilisation + kill avec un allié",
  killAfterHiddenWithAlly: "Kill après s'être caché avec un allié",
  killParticipation: "Participation aux kills",
  pickKillWithAlly: "Kill ciblé avec un allié",
  skillshotsDodged: "Skillshots esquivés",
  skillshotsHit: "Skillshots touchés",
  soloKills: "Kills solo",
  timeCCingOthers: "Temps de contrôle de foule",
  totalAllyJungleMinionsKilled: "Monstres alliés de jungle tués",
  totalDamageDealt: "Dégâts totaux infligés",
  totalDamageDealtToChampions: "Dégâts aux champions",
  totalDamageShieldedOnTeammates: "Boucliers appliqués aux alliés",
  totalDamageTaken: "Dégâts subis",
  totalEnemyJungleMinionsKilled: "Monstres ennemis de jungle tués",
  totalHeal: "Soins totaux",
  totalHealsOnTeammates: "Soins appliqués aux alliés",
  totalMinionsKilled: "Sbires tués",
  totalTimeCCDealt: "Durée totale de CC infligé",
  turretKills: "Tourelles détruites",
  wardsGuarded: "Balises protégées",
  wardsKilled: "Balises ennemies détruites",
  wardsPlaced: "Balises posées"
};


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
            margin={{ top: 20, right: 30, bottom: 80, left: 20 }}
          >
            <XAxis
              dataKey="stat"
              type="category"
              interval={0}
              angle={-30}
              textAnchor="end"
              tickLine={false}
              height={80} // plus d’espace
              tickFormatter={(stat) => STAT_LABELS[stat] || stat}
              tick={{ dy: 10 }} // décale les textes plus bas
            />
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
                dy={-10}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartImpact;
