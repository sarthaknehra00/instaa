"use client";

import { useState, useRef } from "react";
import { Search, Loader2, MessageCircle, ExternalLink } from "lucide-react";

export default function Home() {
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [progressText, setProgressText] = useState("");
  const [results, setResults] = useState<any>(null);
  
  // Track interval ID defensively
  const pollIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username) return;
    
    // Reset state
    setLoading(true);
    setResults(null);
    setProgressText("Waking up worker nodes...");
    
    // Clear any existing intervals
    if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);

    try {
      // 1. Dispatch Scraping Job
      const res = await fetch(`http://localhost:8000/api/v1/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username }),
      });
      const data = await res.json();
      const taskId = data.task_id;
      
      // 2. Poll API for Job Status (Real-time Feedback)
      pollIntervalRef.current = setInterval(async () => {
         try {
             const statusRes = await fetch(`http://localhost:8000/api/v1/jobs/${taskId}`);
             const statusData = await statusRes.json();
             
             if (statusData.progress) {
                 setProgressText(statusData.progress);
             }
             
             if (statusData.status === "completed" || statusData.status === "failed") {
                if (pollIntervalRef.current) clearInterval(pollIntervalRef.current);
                
                // 3. Fetch Final Results once completed
                const commentsRes = await fetch(`http://localhost:8000/api/v1/users/${username}/comments`);
                const commentsData = await commentsRes.json();
                
                setResults(commentsData.comments || []);
                setLoading(false);
             }
         } catch (pollErr) {
             console.error("Polling error:", pollErr);
         }
      }, 1500); // Check status every 1.5 seconds

    } catch (error) {
      console.error("Failed to start job:", error);
      setProgressText("System failure. Could not connect to engine.");
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0A0A0A] text-white flex flex-col items-center py-20 px-4 relative overflow-hidden font-sans">
      {/* Background Glow Elements */}
      <div className="absolute top-[10%] left-[-10%] w-[50%] h-[50%] bg-purple-600/20 blur-[150px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-600/20 blur-[150px] rounded-full pointer-events-none" />

      <h1 className="text-5xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600">
        InstaTrack
      </h1>
      <p className="text-gray-400 mb-10 max-w-md text-center">
        Deep-scan the neural graph. Discover comments made by public Instagram accounts.
      </p>

      <form 
        onSubmit={handleSearch}
        className="w-full max-w-xl group relative z-10"
      >
        <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
        <div className="relative flex items-center bg-[#151515] rounded-2xl p-2 ring-1 ring-white/10 shadow-2xl">
          <div className="pl-4 pr-2 text-gray-400">
            <Search size={20} />
          </div>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="target_username"
            className="w-full bg-transparent border-none outline-none text-white placeholder-gray-600 py-3 font-medium"
          />
          <button 
            type="submit"
            disabled={loading}
            className="bg-white text-black px-6 py-3 rounded-xl font-bold hover:bg-gray-200 transition-colors disabled:opacity-50 flex items-center gap-2"
          >
            {loading && <Loader2 size={16} className="animate-spin" />}
            Analyze
          </button>
        </div>
      </form>

      {/* Results & Loading Container */}
      <div className="w-full max-w-6xl mt-20 z-10">
        
        {loading && (
          <div className="flex flex-col items-center justify-center p-12 bg-[#151515]/50 backdrop-blur-md rounded-3xl border border-white/5 animate-pulse">
            <Loader2 size={40} className="animate-spin mb-6 text-purple-500" />
            <p className="text-xl font-medium text-white">{progressText}</p>
            <p className="text-sm mt-3 text-gray-500 text-center max-w-md">
              Bypassing standard HTML parsers and intercepting GraphQL payloads. This might take a few moments depending on node latency.
            </p>
          </div>
        )}

        {results && !loading && (
          <div className="animate-in fade-in slide-in-from-bottom-10 duration-700">
             <div className="mb-6 flex justify-between items-end border-b border-white/10 pb-4">
                 <h2 className="text-2xl font-bold text-gray-100">Found {results.length} interactions</h2>
                 <span className="text-sm font-mono text-purple-400">@ {username}</span>
             </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {results.map((comment: any, index: number) => (
                <div 
                  key={comment.id || index} 
                  className="group relative rounded-3xl overflow-hidden aspect-[4/5] block ring-1 ring-white/10 hover:ring-purple-500/50 transition-all shadow-2xl flex flex-col"
                >
                  {/* Background Image Container */}
                  <div className="absolute inset-0 z-0">
                    <div 
                      className="absolute inset-0 bg-cover bg-center transition-transform duration-700 group-hover:scale-110"
                      style={{ backgroundImage: `url(${comment.post_thumbnail})` }}
                    />
                    {/* Deep gradient overlay to ensure text is ALWAYS readable */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-transparent opacity-90" />
                  </div>
                  
                  {/* Content Overlay */}
                  <div className="relative z-10 p-6 flex flex-col h-full justify-between">
                    <div className="flex justify-end">
                       <a href={comment.original_post_url} target="_blank" rel="noreferrer" className="bg-white/10 hover:bg-white/20 p-2 rounded-full backdrop-blur-md transition-colors text-white">
                         <ExternalLink size={18} />
                       </a>
                    </div>
                    
                    <div className="w-full">
                      <div className="bg-black/40 backdrop-blur-xl rounded-2xl p-5 border border-white/10 shadow-xl">
                        <div className="flex items-start gap-3 mb-3">
                          <MessageCircle size={20} className="text-purple-400 mt-0.5 shrink-0" />
                          <p className="text-base text-gray-100 font-medium leading-relaxed">
                            {comment.text}
                          </p>
                        </div>
                        <div className="flex items-center justify-between text-xs font-mono mt-4 pt-4 border-t border-white/10">
                           <span className="text-gray-400">
                             {new Date(comment.timestamp).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}
                           </span>
                           <span className="text-blue-400/80 bg-blue-500/10 px-2 py-1 rounded-md">{comment.source || "Network"}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            {results.length === 0 && (
                <div className="text-center p-12 bg-[#151515] rounded-3xl border border-white/5">
                    <p className="text-xl text-gray-400">No public comments found for this user.</p>
                </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
