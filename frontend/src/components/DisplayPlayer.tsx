import React, { useEffect, useState, useRef, useLayoutEffect } from "react";
import { AlertTriangle, Loader2 } from "lucide-react";

function WidgetRenderer({ widget }: { widget: any }) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (widget.widget_type === "static") return;
    const fetchData = async () => {
      try {
        const res = await fetch(widget.content);
        const json = await res.json();
        setData(json);
      } catch (e) {
        console.error("Fetch error:", e);
      } finally {
        setLoading(false);
      }
    };
    setLoading(true);
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [widget.content, widget.widget_type]);

  if (loading && !data)
    return <Loader2 className="animate-spin text-slate-300" size={40} />;

  switch (widget.widget_type) {
    case "static":
      return (
        <div className="text-2xl text-slate-600 font-medium leading-relaxed overflow-hidden">
          {widget.content}
        </div>
      );

    case "news":
      const newsItems = Array.isArray(data)
        ? data
        : data?.news?.all?.data?.items || [];
      return (
        <div className="w-full space-y-4 overflow-hidden">
          {newsItems.slice(0, 2).map((item: any, i: number) => (
            <div key={i} className="border-l-4 border-cyan-500 pl-4">
              <div className="font-bold text-xl text-slate-800 line-clamp-1">
                {item.title}
              </div>
              <div
                className="text-slate-500 text-sm line-clamp-2 mt-1"
                dangerouslySetInnerHTML={{ __html: item.text }}
              />
            </div>
          ))}
        </div>
      );

    case "parking":
    case "storage":
      return (
        <div className="flex flex-col items-start">
          <div className="text-7xl font-black text-slate-900 tracking-tighter">
            {data?.unassigned_count ?? 0}{" "}
            <span className="text-slate-300 font-light">/</span>{" "}
            {data?.total_count ?? 0}
          </div>
          <div className="text-sm uppercase tracking-widest text-slate-400 font-bold mt-2">
            машиномест доступно
          </div>
        </div>
      );

    default:
      return <div className="text-slate-300 italic">Контент не настроен</div>;
  }
}

export default function DisplayPlayer({ slug }: { slug: string }) {
  const [config, setConfig] = useState<any>(null);
  const [emergency, setEmergency] = useState<{ active: boolean; text: string }>(
    { active: false, text: "" },
  );

  const [isTwoLines, setIsTwoLines] = useState(false);
  const textRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (emergency.active && textRef.current) {
      const el = textRef.current;
      setIsTwoLines(false);

      const checkWrap = () => {
        const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
        if (el.scrollHeight > fontSize * 1.4) {
          setIsTwoLines(true);
        }
      };

      const timer = setTimeout(checkWrap, 50);
      return () => clearTimeout(timer);
    }
  }, [emergency.text, emergency.active]);

  useEffect(() => {
    fetch(`/api/v1/screens/${slug}`)
      .then((res) => res.json())
      .then((data) => {
        setConfig(data);
        if (data.is_emergency)
          setEmergency({ active: true, text: data.emergency_text || "" });

        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        const ws = new WebSocket(
          `${protocol}//${window.location.host}/ws/${data.id}`,
        );
        ws.onmessage = (e) => {
          const msg = JSON.parse(e.data);
          if (msg.type === "EMERGENCY_UPDATE") {
            setEmergency({
              active: msg.payload.is_emergency,
              text: msg.payload.text || "",
            });
          }
        };
        return () => ws.close();
      });
  }, [slug]);

  if (!config)
    return (
      <div className="h-screen w-screen bg-[#f1f5f9] flex items-center justify-center text-slate-400 font-bold">
        ЗАГРУЗКА ДИСПЛЕЯ...
      </div>
    );

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#f1f5f9] font-sans">
      {emergency.active && (
        <div
          className="flex-shrink-0 w-full bg-[#FF0000] flex items-center px-12 gap-6 border-b-4 border-black/10 transition-[height] duration-300"
          style={{ height: isTwoLines ? "10vh" : "5vh" }}
        >
          <AlertTriangle
            className="text-white flex-shrink-0"
            size={isTwoLines ? "5vh" : "3.5vh"}
          />
          <div
            ref={textRef}
            className="text-white font-black uppercase tracking-tight text-left break-words overflow-hidden"
            style={{
              fontSize: isTwoLines ? "3.5vw" : "4.2vw",
              lineHeight: "1",
              WebkitLineClamp: 2,
              display: "-webkit-box",
              WebkitBoxOrient: "vertical",
            }}
          >
            Режим ЧС: {emergency.text}
          </div>
        </div>
      )}

      <div className="flex-1 p-8 overflow-hidden">
        <div className="grid h-full w-full grid-cols-2 grid-rows-2 gap-8">
          {[0, 1, 2, 3].map((idx) => {
            const slot = config.slots[idx.toString()] || config.slots[idx];
            return (
              <div
                key={idx}
                className="bg-white rounded-[2.5rem] shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] border border-white p-10 flex flex-col items-start overflow-hidden relative"
              >
                {slot ? (
                  <>
                    <h3 className="text-sm font-black uppercase tracking-[0.2em] text-slate-400 mb-6 flex-shrink-0">
                      {slot.title || slot.widget_type}
                    </h3>
                    <div className="w-full flex-1 flex flex-col justify-center overflow-hidden">
                      <WidgetRenderer widget={slot} />
                    </div>
                  </>
                ) : (
                  <div className="m-auto text-slate-200 font-black tracking-widest uppercase text-xs">
                    Блок {idx + 1} свободен
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
