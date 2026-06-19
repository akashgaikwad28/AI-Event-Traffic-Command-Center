import React, { useEffect, useRef } from 'react';
import { useDemoStore } from '../../store/demo.store';

export const SimulationTimeline: React.FC = () => {
  const {
    simulationResult,
    playbackState,
    playbackSpeed,
    playbackFrameIndex,
    setPlaybackState,
    setPlaybackSpeed,
    setPlaybackFrame
  } = useDemoStore();

  const frames = simulationResult?.optimized_state?.timeline_frames || [];
  const maxFrames = frames.length;
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (playbackState === 'PLAYING' && maxFrames > 0) {
      intervalRef.current = window.setInterval(() => {
        setPlaybackFrame(Math.min(playbackFrameIndex + 1, maxFrames - 1));
        if (playbackFrameIndex >= maxFrames - 2) {
          setPlaybackState('STOPPED');
        }
      }, 1000 / playbackSpeed);
    } else if (intervalRef.current !== null) {
      clearInterval(intervalRef.current);
    }
    return () => {
      if (intervalRef.current !== null) clearInterval(intervalRef.current);
    };
  }, [playbackState, playbackFrameIndex, playbackSpeed, maxFrames, setPlaybackFrame, setPlaybackState]);

  if (!simulationResult || maxFrames === 0) return null;

  const currentFrame = frames[playbackFrameIndex];

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 my-4 shadow-lg backdrop-blur-sm bg-opacity-80">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-white font-bold flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          Timeline Playback
        </h3>
        <div className="flex items-center gap-4">
          <span className="text-slate-400 text-sm">T+{currentFrame.time_offset_mins} mins</span>
          <div className="flex bg-slate-900 rounded p-1 gap-1">
            {[1, 2, 5, 10].map(s => (
              <button
                key={s}
                className={`px-2 py-1 text-xs rounded transition-colors ${playbackSpeed === s ? 'bg-blue-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-700'}`}
                onClick={() => setPlaybackSpeed(s)}
              >
                {s}x
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button
          onClick={() => setPlaybackState(playbackState === 'PLAYING' ? 'PAUSED' : 'PLAYING')}
          className="w-10 h-10 rounded-full bg-blue-600 hover:bg-blue-500 text-white flex items-center justify-center transition-transform hover:scale-105 active:scale-95"
        >
          {playbackState === 'PLAYING' ? (
             <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/></svg>
          ) : (
             <svg className="w-4 h-4 fill-current ml-1" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          )}
        </button>
        <button
          onClick={() => { setPlaybackFrame(0); setPlaybackState('STOPPED'); }}
          className="p-2 text-slate-400 hover:text-white transition-colors"
        >
           <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/></svg>
        </button>

        <div className="flex-1 relative mx-4">
          <input
            type="range"
            min={0}
            max={maxFrames - 1}
            value={playbackFrameIndex}
            onChange={(e) => {
              setPlaybackState('PAUSED');
              setPlaybackFrame(Number(e.target.value));
            }}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-500"
          />
        </div>
      </div>
    </div>
  );
};
