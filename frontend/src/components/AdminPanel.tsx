import React, { useState, useEffect } from "react";
import {
    Home, Folder, ChevronDown, ChevronRight,
    Monitor, Copy, ArrowUp, AlertTriangle, Loader2
} from "lucide-react";
import clsx from "clsx";

export default function AdminPanel() {
    const [screens, setScreens] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    const [templates, setTemplates] = useState<any[]>([]);
    const [assigningSlot, setAssigningSlot] = useState<{ sId: string, idx: number } | null>(null);

    const [emergencyInputs, setEmergencyInputs] = useState<Record<string, string>>({});

    const [expanded, setExpanded] = useState<Record<string, boolean>>({});

    useEffect(() => {
        Promise.all([
            fetch("/api/v1/screens/").then(res => res.json()),
            fetch("/api/v1/templates/").then(res => res.json())
        ]).then(([sData, tData]) => {
            setScreens(Array.isArray(sData) ? sData : []);
            setTemplates(Array.isArray(tData) ? tData : []);
            setLoading(false);
        }).catch(() => setLoading(false));
    }, []);

    const toggle = (id: string) => {
        setExpanded(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const handleAssign = async (screenId: string, slotIdx: number, templateId: string | null) => {
        const url = `/api/v1/screens/${screenId}/slots/${slotIdx}${templateId ? `?template_id=${templateId}` : ''}`;
        try {
            await fetch(url, { method: "POST" });

            const res = await fetch(`/api/v1/screens/${screens.find(s => s.id === screenId).slug}`);
            const updatedScreen = await res.json();

            setScreens(prev => prev.map(s => s.id === screenId ? updatedScreen : s));
            setAssigningSlot(null);
        } catch (e) {
            alert("Ошибка при обновлении слота");
        }
    };

    const handleSendEmergency = async (screenId: string, isActive: boolean) => {
        const text = emergencyInputs[screenId] || "ВНИМАНИЕ! ЧРЕЗВЫЧАЙНАЯ СИТУАЦИЯ";
        try {
            await fetch("/api/v1/screens/emergency", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    is_emergency: isActive,
                    emergency_text: isActive ? text : "",
                    screen_ids: [screenId]
                })
            });

            const res = await fetch(`/api/v1/screens/${screens.find(s => s.id === screenId).slug}`);
            const updatedScreen = await res.json();
            setScreens(prev => prev.map(s => s.id === screenId ? updatedScreen : s));

            if (isActive) alert("Сигнал ЧС отправлен");
        } catch (e) {
            alert("Ошибка при отправке ЧС");
        }
    };

    const grouped = screens.reduce((acc: any, screen) => {
        const cId = screen.complex_id || 0;
        const bId = screen.building_id || 0;
        if (!acc[cId]) acc[cId] = { id: cId, title: `Жилой комплекс ${cId}`, buildings: {} };
        if (!acc[cId].buildings[bId]) acc[cId].buildings[bId] = { id: bId, title: `Корпус ${bId}`, screens: [] };
        acc[cId].buildings[bId].screens.push(screen);
        return acc;
    }, {});

    if (loading) return <div className="flex h-screen items-center justify-center bg-[#f1f5f9]"><Loader2 className="animate-spin text-slate-400" size={40} /></div>;

    return (
        <div className="flex min-h-screen bg-[#f1f5f9] font-sans text-slate-900">
            <aside className="fixed left-0 top-0 h-screen w-16 border-r border-slate-200 bg-white flex flex-col items-center py-6 z-30">
                <div className="text-[10px] font-black mb-10">Logo</div>
                <nav className="flex flex-col gap-4">
                    <button className="p-3 rounded-xl bg-[#cffafe] text-[#0891b2] shadow-sm"><Home size={20} strokeWidth={2} /></button>
                    <button className="p-3 rounded-xl text-slate-400 hover:bg-slate-50 transition-colors"><Folder size={20} strokeWidth={2} /></button>
                </nav>
            </aside>

            <main className="ml-16 p-10 w-full max-w-[1440px]">
                <div className="mb-6 flex items-center px-10 text-[13px] font-medium text-slate-400">
                    <div className="w-[35%]">Жилые комплексы</div>
                    <div className="w-[25%] flex items-center gap-1"><Monitor size={14} /> Адрес</div>
                    <div className="w-[15%] flex items-center gap-1"><ArrowUp size={14} /> Аптайм</div>
                    <div className="w-[15%] flex items-center gap-1"><Folder size={14} /> ID объекта</div>
                    <div className="ml-auto flex items-center gap-1"><Plus size={14} /> Загрузка</div>
                </div>

                <div className="space-y-4">
                    {Object.values(grouped).map((complex: any) => (
                        <div key={complex.id} className="rounded-[2.5rem] bg-white shadow-[0_2px_15px_-3px_rgba(0,0,0,0.07)] overflow-hidden">
                            <div className="flex items-center px-10 py-7 cursor-pointer hover:bg-slate-50/50 transition-colors" onClick={() => toggle(`c-${complex.id}`)}>
                                <div className="w-[35%] flex items-center gap-4">
                                    {expanded[`c-${complex.id}`] ? <ChevronDown size={20} className="text-slate-400" /> : <ChevronRight size={20} className="text-slate-400" />}
                                    <span className="text-2xl font-bold tracking-tight">{complex.title}</span>
                                </div>
                                <div className="w-[25%] text-slate-500 text-sm">ул. Уличная, д. 15, к. 1-2</div>
                                <div className="w-[15%]"><StatusBadge status="Проблемы" /></div>
                                <div className="w-[15%] flex items-center gap-2 text-slate-400 font-mono text-sm">jk{complex.id} <Copy size={14} className="cursor-pointer hover:text-slate-600" /></div>
                                <button className="ml-auto bg-[#f8fafc] border border-slate-100 px-6 py-2.5 rounded-2xl text-[13px] font-bold text-slate-700 hover:shadow-sm transition-all">Загрузить</button>
                            </div>

                            {expanded[`c-${complex.id}`] && (
                                <div className="bg-[#f8fafc]/50 px-6 pb-6 space-y-3">
                                    {Object.values(complex.buildings).map((building: any) => (
                                        <div key={building.id} className="rounded-[2rem] bg-white border border-slate-100 shadow-sm overflow-hidden">
                                            <div className="flex items-center px-10 py-6 cursor-pointer" onClick={() => toggle(`b-${building.id}`)}>
                                                <div className="w-[35%] flex items-center gap-4 pl-8">
                                                    {expanded[`b-${building.id}`] ? <ChevronDown size={18} className="text-slate-400" /> : <ChevronRight size={18} className="text-slate-400" />}
                                                    <span className="text-xl font-bold text-slate-800">{building.title}</span>
                                                </div>
                                                <div className="w-[25%] text-slate-500 text-sm">ул. Уличная, д. 15, к. 1</div>
                                                <div className="w-[15%]"><StatusBadge status="Работает" /></div>
                                                <div className="w-[15%] flex items-center gap-2 text-slate-400 font-mono text-xs">bld{building.id} <Copy size={12} /></div>
                                                <button className="ml-auto bg-[#f8fafc] border border-slate-100 px-6 py-2 rounded-2xl text-[13px] font-bold">Загрузить</button>
                                            </div>

                                            {expanded[`b-${building.id}`] && (
                                                <div className="px-10 pb-6 space-y-3">
                                                    {building.screens.map((screen: any) => (
                                                        <div key={screen.id} className="rounded-3xl border border-slate-50 overflow-hidden">
                                                            <div className="flex items-center px-10 py-5 bg-white cursor-pointer hover:bg-slate-50/50" onClick={() => toggle(`s-${screen.id}`)}>
                                                                <div className="w-[35%] flex items-center gap-4 pl-16">
                                                                    {expanded[`s-${screen.id}`] ? <ChevronDown size={16} className="text-slate-400" /> : <ChevronRight size={16} className="text-slate-400" />}
                                                                    <span className="text-lg font-bold text-slate-700">{screen.name}</span>
                                                                </div>
                                                                <div className="w-[25%] text-slate-500 text-sm italic">{screen.slug}</div>
                                                                <div className="w-[15%]"><StatusBadge status={screen.is_emergency ? "Проблемы" : "Работает"} /></div>
                                                                <div className="w-[15%] flex items-center gap-2 text-slate-400 font-mono text-xs uppercase">scr{screen.id.slice(0, 5)} <Copy size={12} /></div>
                                                                <button className="ml-auto bg-[#f8fafc] border border-slate-100 px-6 py-2 rounded-2xl text-[13px] font-bold">Загрузить</button>
                                                            </div>

                                                            {expanded[`s-${screen.id}`] && (
                                                                <div className="p-10 bg-slate-50/30 border-t border-slate-50">
                                                                    <div className="flex items-center gap-4 mb-8">
                                                                        <h3 className="text-lg font-bold text-slate-800">Контент на экране</h3>
                                                                        <span className="bg-[#dcfce7] text-[#166534] px-3 py-1 rounded-xl text-[11px] font-black uppercase tracking-tight flex items-center gap-1">
                                                                            <span className="w-1.5 h-1.5 bg-[#166534] rounded-full animate-pulse"></span> В эфире
                                                                        </span>
                                                                    </div>

                                                                    <div className="space-y-3 mb-8">
                                                                        {[0, 1, 2, 3].map(idx => {
                                                                            const slot = screen.slots[idx];
                                                                            return (
                                                                                <div key={idx} className="flex items-center bg-white px-8 py-5 rounded-[1.5rem] shadow-sm">
                                                                                    <div className="w-40 text-[11px] font-bold text-slate-300 uppercase tracking-widest flex items-center gap-2">
                                                                                        <ArrowUp size={14} /> {slot ? (idx === 0 ? "Реклама" : "Системное") : "Пусто"}
                                                                                    </div>
                                                                                    <div className="w-1/3 font-bold text-slate-800 text-lg">
                                                                                        {slot?.title || "Блок не настроен"}
                                                                                    </div>
                                                                                    <div className="flex-grow text-sm text-slate-400 font-medium">
                                                                                        {slot ? (idx === 0 ? "Активно до 06.07.26" : "Автообновление") : "—"}
                                                                                    </div>
                                                                                    <div className="flex gap-2 relative">
                                                                                        {assigningSlot?.sId === screen.id && assigningSlot?.idx === idx ? (
                                                                                            <div className="absolute right-0 bottom-full mb-2 w-64 bg-white shadow-xl rounded-2xl border border-slate-200 z-50 p-2 space-y-1">
                                                                                                <div className="text-[10px] font-black uppercase text-slate-400 px-3 py-1">Выберите шаблон</div>
                                                                                                <div className="max-h-48 overflow-y-auto">
                                                                                                    {templates.map(t => (
                                                                                                        <button
                                                                                                            key={t.id}
                                                                                                            onClick={() => handleAssign(screen.id, idx, t.id)}
                                                                                                            className="w-full text-left px-3 py-2 hover:bg-slate-50 rounded-xl text-xs font-bold transition-colors"
                                                                                                        >
                                                                                                            {t.name}
                                                                                                        </button>
                                                                                                    ))}
                                                                                                </div>
                                                                                                <button onClick={() => setAssigningSlot(null)} className="w-full text-slate-400 text-[10px] font-bold py-1 border-t mt-1">Отмена</button>
                                                                                            </div>
                                                                                        ) : null}

                                                                                        <button
                                                                                            onClick={() => setAssigningSlot({ sId: screen.id, idx })}
                                                                                            className="bg-[#2d3748] text-white px-6 py-2 rounded-xl text-[13px] font-bold hover:bg-black transition-colors"
                                                                                        >
                                                                                            Заменить
                                                                                        </button>

                                                                                        <button
                                                                                            onClick={() => handleAssign(screen.id, idx, null)}
                                                                                            className="bg-[#fee2e2] text-[#b91c1c] px-6 py-2 rounded-xl text-[13px] font-bold hover:bg-red-100"
                                                                                        >
                                                                                            Удалить
                                                                                        </button>
                                                                                    </div>
                                                                                </div>
                                                                            );
                                                                        })}
                                                                    </div>

                                                                    <div className="flex items-center justify-between bg-white px-10 py-4 rounded-[2rem] border border-slate-100 shadow-inner">
                                                                        <input
                                                                            type="text"
                                                                            placeholder="Введите текст оповещения о ЧС..."
                                                                            value={emergencyInputs[screen.id] || ""}
                                                                            onChange={(e) => setEmergencyInputs(prev => ({ ...prev, [screen.id]: e.target.value }))}
                                                                            className="text-slate-600 font-medium bg-transparent outline-none flex-grow px-6 placeholder:italic placeholder:text-slate-300"
                                                                        />
                                                                        <div className="flex gap-2 pr-2">
                                                                            {screen.is_emergency && (
                                                                                <button
                                                                                    onClick={() => handleSendEmergency(screen.id, false)}
                                                                                    className="bg-slate-100 text-slate-500 px-6 py-2.5 rounded-2xl text-[13px] font-black hover:bg-slate-200 transition-all"
                                                                                >
                                                                                    Сбросить
                                                                                </button>
                                                                            )}
                                                                            <button
                                                                                onClick={() => handleSendEmergency(screen.id, true)}
                                                                                className={clsx(
                                                                                    "px-8 py-2.5 rounded-2xl text-[13px] font-black transition-all border",
                                                                                    screen.is_emergency
                                                                                        ? "bg-red-600 text-white border-red-600 shadow-lg shadow-red-200"
                                                                                        : "bg-white border-slate-200 text-slate-600 hover:bg-slate-50"
                                                                                )}
                                                                            >
                                                                                {screen.is_emergency ? "Обновить ЧС" : "Загрузить"}
                                                                            </button>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </main>
        </div>
    );
}

function StatusBadge({ status }: { status: "Работает" | "Проблемы" }) {
    const isOk = status === "Работает";
    return (
        <span className={clsx(
            "px-5 py-1.5 rounded-2xl text-[12px] font-bold transition-all border",
            isOk
                ? "bg-[#f0fdf4] text-[#16a34a] border-[#dcfce7]"
                : "bg-[#fff1f2] text-[#e11d48] border-[#ffe4e6]"
        )}>
            {status}
        </span>
    );
}

function Plus({ size, className }: { size: number, className?: string }) {
    return (
        <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className={className}>
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
    );
}