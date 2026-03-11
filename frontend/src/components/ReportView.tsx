"use client";

import { useMemo } from "react";
import ReactMarkdown from "react-markdown";

interface ReportViewProps {
  data: any;
  onReset: () => void;
}

export default function ReportView({ data, onReset }: ReportViewProps) {
  const { filename, content_type, analysis, ai_summary, email_sent } = data;
  const { summary, numeric_metrics, categorical_metrics } = analysis;

  const numericKeys = useMemo(() => Object.keys(numeric_metrics || {}), [numeric_metrics]);
  const categoricalKeys = useMemo(() => Object.keys(categorical_metrics || {}), [categorical_metrics]);

  return (
    <div className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-2xl p-6 lg:p-10 shadow-2xl w-full max-w-5xl mx-auto space-y-8 animate-[fadeIn_0.5s_ease-out]">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-white/10 pb-6 gap-4">
        <div>
          <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-blue-300 tracking-tight">
            Analysis Report
          </h2>
          <p className="text-purple-200/80 mt-1 font-mono text-sm">
            {filename} <span className="text-purple-400">({content_type})</span>
          </p>
        </div>
        <button
          onClick={onReset}
          className="px-6 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full text-white font-medium transition-all shadow-lg text-sm flex items-center gap-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path></svg>
          Analyze Another
        </button>
      </div>

      {email_sent && (
        <div className="bg-emerald-500/20 border border-emerald-500/50 text-emerald-200 px-5 py-4 rounded-xl flex items-center gap-3">
          <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <p className="font-medium">Report has been emailed successfully!</p>
        </div>
      )}

      {ai_summary && (
        <div className="bg-gradient-to-br from-indigo-900/50 to-purple-900/50 border border-indigo-400/30 rounded-2xl p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-10">
            <svg className="w-32 h-32" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 22h20L12 2zm0 4.2l6.8 13.8H5.2L12 6.2z"/></svg>
          </div>
          <h3 className="text-xl font-bold text-indigo-300 mb-4 flex items-center gap-2">
            <span className="text-2xl">✨</span> AI Insights
          </h3>
          <div className="prose prose-invert prose-p:text-indigo-100/90 prose-p:leading-relaxed prose-headings:text-indigo-200 prose-strong:text-indigo-300 max-w-none relative z-10 whitespace-pre-wrap">
            <ReactMarkdown>{ai_summary}</ReactMarkdown>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white/5 border border-white/10 p-5 rounded-2xl flex flex-col justify-center items-center text-center">
          <p className="text-purple-300/70 text-sm font-medium uppercase tracking-wider mb-2">Total Rows</p>
          <p className="text-4xl font-bold text-white">{summary.total_rows.toLocaleString()}</p>
        </div>
        <div className="bg-white/5 border border-white/10 p-5 rounded-2xl flex flex-col justify-center items-center text-center">
          <p className="text-purple-300/70 text-sm font-medium uppercase tracking-wider mb-2">Total Columns</p>
          <p className="text-4xl font-bold text-white">{summary.total_columns}</p>
        </div>
        <div className="bg-white/5 border border-white/10 p-5 rounded-2xl flex flex-col justify-center items-center text-center">
          <p className="text-purple-300/70 text-sm font-medium uppercase tracking-wider mb-2">Numeric Cols</p>
          <p className="text-4xl font-bold text-white">{numericKeys.length}</p>
        </div>
        <div className="bg-white/5 border border-white/10 p-5 rounded-2xl flex flex-col justify-center items-center text-center">
          <p className="text-purple-300/70 text-sm font-medium uppercase tracking-wider mb-2">Categorical Cols</p>
          <p className="text-4xl font-bold text-white">{categoricalKeys.length}</p>
        </div>
      </div>

      <div className="space-y-8">
        {numericKeys.length > 0 && (
          <div>
            <h3 className="text-xl font-semibold text-purple-200 mb-4 border-b border-white/10 pb-2">Numeric Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {numericKeys.map((col) => (
                <div key={col} className="bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                  <h4 className="font-mono text-purple-300 mb-3 truncate" title={col}>{col}</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between border-b border-white/5 pb-1">
                      <span className="text-white/50">Mean</span>
                      <span className="text-white/90 font-mono">{numeric_metrics[col].mean.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between border-b border-white/5 pb-1">
                      <span className="text-white/50">Min / Max</span>
                      <span className="text-white/90 font-mono">{numeric_metrics[col].min} → {numeric_metrics[col].max}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-white/50">Std Dev</span>
                      <span className="text-white/90 font-mono">{numeric_metrics[col].std_dev.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {categoricalKeys.length > 0 && (
          <div>
            <h3 className="text-xl font-semibold text-purple-200 mb-4 border-b border-white/10 pb-2">Categorical Top Values</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 xlg:grid-cols-3 gap-4">
              {categoricalKeys.map((col) => (
                <div key={col} className="bg-white/5 border border-white/10 rounded-xl p-4 hover:bg-white/10 transition-colors">
                  <div className="flex justify-between items-center mb-3">
                    <h4 className="font-mono text-purple-300 truncate w-2/3" title={col}>{col}</h4>
                    <span className="text-xs font-bold bg-white/10 text-white/70 px-2 py-1 rounded-md">
                      {categorical_metrics[col].unique_values_count} Unique
                    </span>
                  </div>
                  <ul className="space-y-1.5 text-sm">
                    {Object.entries(categorical_metrics[col].top_5_values).map(([val, count]: any) => (
                      <li key={val} className="flex justify-between items-center px-2 py-1 bg-white/5 rounded">
                        <span className="text-white/80 truncate w-3/4 pr-2" title={val === "nan" ? "Empty/NaN" : val}>
                          {val === "nan" ? <i className="text-white/40">Empty/NaN</i> : val}
                        </span>
                        <span className="text-white font-mono bg-purple-500/30 px-2 py-0.5 rounded text-xs">{count}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
