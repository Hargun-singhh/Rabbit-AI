"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ReportView from "@/components/ReportView";

export default function Home() {
  const [reportData, setReportData] = useState<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  return (
    <main className="min-h-screen relative overflow-hidden bg-slate-950 font-sans">
      {/* Dynamic Background Effects */}
      <div className="fixed inset-0 min-h-screen w-full pointer-events-none z-0">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-600/30 blur-[120px] rounded-full mix-blend-screen animate-pulse duration-10000"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-600/20 blur-[150px] rounded-full mix-blend-screen delay-1000"></div>
        <div className="absolute top-[30%] left-[50%] w-[30%] h-[30%] bg-fuchsia-600/20 blur-[100px] rounded-full mix-blend-screen delay-3000"></div>
      </div>

      <div className="relative z-10 container flex flex-col items-center justify-center mx-auto px-4 py-16 min-h-screen">
        {!reportData && (
          <div className="text-center max-w-2xl mb-12 animate-[fadeIn_0.5s_ease-out]">
            <div className="inline-block px-4 py-1.5 rounded-full bg-white/5 border border-white/10 text-purple-300 text-sm font-medium mb-6 backdrop-blur-md">
              AI-Powered Data Analysis
            </div>
            <h1 className="text-5xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-300 to-blue-400 tracking-tight leading-tight mb-6">
              Turn Spreadsheets <br/>into Insights.
            </h1>
            <p className="text-lg text-purple-200/80 mb-8 max-w-xl mx-auto">
              Upload your CSV or Excel files. Our backend crunches the numbers while Gemini AI spots trends and generates comprehensible summaries instantly.
            </p>
          </div>
        )}

        <div className="w-full transition-all duration-500 ease-in-out">
          {!reportData ? (
            <UploadForm 
              onUploadSuccess={setReportData} 
              isProcessing={isProcessing}
              setIsProcessing={setIsProcessing} 
            />
          ) : (
            <ReportView 
              data={reportData} 
              onReset={() => setReportData(null)} 
            />
          )}
        </div>
      </div>
    </main>
  );
}
