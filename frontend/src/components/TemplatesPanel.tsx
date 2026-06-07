import React, { useState, useEffect } from "react";
import {
  Home,
  Folder,
  ChevronDown,
  Plus,
  Info,
  Loader2,
  X,
  Trash2,
} from "lucide-react";

interface TemplatesPanelProps {
  onNavigate: (path: string) => void;
}

export default function TemplatesPanel({ onNavigate }: TemplatesPanelProps) {
  const [templates, setTemplates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    name: "",
    widget_type: "static",
    title: "",
    content: "",
  });

  const loadTemplates = async () => {
    try {
      const res = await fetch(`/api/v1/templates/?t=${Date.now()}`, {
        cache: "no-store",
        headers: { Pragma: "no-cache" },
      });
      const data = await res.json();
      setTemplates(Array.isArray(data) ? [...data] : []);
    } catch (e) {
      console.error("Failed to load templates", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTemplates();
  }, []);

  const openCreateModal = () => {
    setEditingId(null);
    setFormData({ name: "", widget_type: "static", title: "", content: "" });
    setIsModalOpen(true);
  };

  const openEditModal = (template: any) => {
    setEditingId(template.id);
    setFormData({
      name: template.name,
      widget_type: template.widget_type,
      title: template.title || "",
      content: template.content,
    });
    setIsModalOpen(true);
  };

  const handleTypeChange = (type: string) => {
    let newContent = "";
    if (type === "news") newContent = "/api/v1/data/news";
    else if (type === "parking") newContent = "/api/v1/data/parking";
    else if (type === "storage") newContent = "/api/v1/data/storage";

    setFormData({ ...formData, widget_type: type, content: newContent });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);

    const url = editingId
      ? `/api/v1/templates/?template_id=${editingId}`
      : "/api/v1/templates/";
    const method = editingId ? "PATCH" : "POST";

    try {
      const res = await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (res.ok) {
        setIsModalOpen(false);
        setTimeout(loadTemplates, 100);
      } else {
        const errorData = await res.json();
        console.error("Server Error:", errorData);
        alert(
          `Ошибка сервера: ${JSON.stringify(errorData.detail || errorData)}`,
        );
      }
    } catch (e) {
      console.error("Network Error:", e);
      alert("Сетевая ошибка при сохранении");
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async () => {
    if (
      !editingId ||
      !window.confirm(
        "Удалить этот шаблон? Экраны, использующие его, станут пустыми.",
      )
    )
      return;
    setIsSaving(true);
    try {
      const res = await fetch(`/api/v1/templates/${editingId}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setIsModalOpen(false);
        setTimeout(loadTemplates, 100);
      }
    } catch (e) {
      alert("Ошибка при удалении");
    } finally {
      setIsSaving(false);
    }
  };

  if (loading)
    return (
      <div className="flex h-screen items-center justify-center bg-[#f1f5f9]">
        <Loader2 className="animate-spin text-slate-300" size={48} />
      </div>
    );

  return (
    <div className="flex min-h-screen bg-[#f1f5f9] font-sans text-slate-900">
      <aside className="fixed left-0 top-0 h-screen w-16 border-r border-slate-200 bg-white flex flex-col items-center py-6 z-30">
        <div className="text-[10px] font-black mb-10 tracking-tighter">
          Logo
        </div>
        <nav className="flex flex-col gap-4">
          <button
            onClick={() => onNavigate("/")}
            className="p-3 rounded-xl text-slate-400 hover:bg-slate-50 transition-all"
          >
            <Home size={22} strokeWidth={2} />
          </button>
          <button
            onClick={() => onNavigate("/templates")}
            className="p-3 rounded-xl bg-[#cffafe] text-[#0891b2] shadow-sm shadow-cyan-100"
          >
            <Folder size={22} strokeWidth={2.5} />
          </button>
        </nav>
      </aside>

      <main className="ml-16 p-10 w-full max-w-[1600px]">
        <div className="flex items-center gap-6 mb-10">
          <h1 className="text-4xl font-black text-slate-900 tracking-tight">
            Виджеты
          </h1>
          <button
            onClick={openCreateModal}
            className="bg-[#06b6d4] hover:bg-[#0891b2] text-white px-8 py-3 rounded-2xl text-[14px] font-black flex items-center gap-2 transition-all shadow-lg shadow-cyan-100 uppercase tracking-tight"
          >
            <Plus size={20} strokeWidth={3} /> Создать
          </button>
        </div>

        <div className="rounded-[2.5rem] bg-white shadow-[0_4px_25px_-5px_rgba(0,0,0,0.03)] border border-white overflow-hidden">
          <div className="flex items-center justify-between px-10 py-8 border-b border-slate-50">
            <div className="flex items-center gap-4">
              <ChevronDown size={24} className="text-slate-300" />
              <span className="text-xl font-bold text-slate-800 tracking-tight">
                Все доступные шаблоны
              </span>
            </div>
            <span className="text-slate-400 text-xs font-black uppercase tracking-[0.2em]">
              {templates.length} объектов в базе
            </span>
          </div>

          <div className="p-10 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-10">
            {templates.map((t) => (
              <div
                key={t.id}
                onClick={() => openEditModal(t)}
                className="flex flex-col group cursor-pointer"
              >
                <div className="aspect-[3/4] bg-[#f8fafc] rounded-[2.2rem] border-2 border-transparent shadow-sm mb-4 p-6 flex flex-col relative overflow-hidden group-hover:border-[#06b6d4] group-hover:bg-white transition-all duration-300 group-hover:-translate-y-1">
                  {t.widget_type === "parking" ||
                  t.widget_type === "storage" ? (
                    <div className="flex flex-col items-center justify-center h-full gap-4 opacity-20">
                      <div className="grid grid-cols-4 gap-1.5">
                        {[...Array(12)].map((_, i) => (
                          <div
                            key={i}
                            className="w-2 h-2 rounded-full bg-cyan-600"
                          />
                        ))}
                      </div>
                      <div className="text-[10px] font-black text-cyan-600 uppercase tracking-widest text-center">
                        Status_Data
                      </div>
                    </div>
                  ) : t.widget_type === "news" ? (
                    <div className="space-y-3 opacity-30 mt-4 px-2">
                      <div className="h-3 w-4/5 bg-slate-300 rounded-full" />
                      <div className="space-y-2">
                        <div className="h-1.5 w-full bg-slate-200 rounded-full" />
                        <div className="h-1.5 w-full bg-slate-200 rounded-full" />
                        <div className="h-1.5 w-2/3 bg-slate-200 rounded-full" />
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <Info
                        size={40}
                        className="text-slate-200"
                        strokeWidth={1.5}
                      />
                    </div>
                  )}

                  <div className="absolute inset-0 bg-[#0891b2]/90 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity duration-300">
                    <span className="text-white text-[11px] font-black uppercase tracking-[0.2em] border-2 border-white/30 px-4 py-2 rounded-xl">
                      Настроить
                    </span>
                  </div>
                </div>

                <div className="text-[14px] font-bold text-slate-800 text-center px-2 line-clamp-2 leading-tight mb-1">
                  {t.name}
                </div>
                <div className="text-[10px] text-slate-400 font-black uppercase text-center tracking-widest opacity-60">
                  {t.widget_type}
                </div>
              </div>
            ))}

            {templates.length === 0 && (
              <div className="col-span-full py-32 text-center flex flex-col items-center opacity-20">
                <Folder size={64} strokeWidth={1} className="mb-4" />
                <div className="font-black uppercase tracking-widest text-sm">
                  No_Templates_Found
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-6">
          <div
            className="absolute inset-0 bg-slate-900/60 backdrop-blur-md animate-in fade-in duration-300"
            onClick={() => setIsModalOpen(false)}
          />
          <div className="relative bg-white w-full max-w-lg rounded-[3rem] shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300">
            <div className="px-10 py-8 border-b border-slate-50 flex justify-between items-center">
              <h2 className="text-2xl font-black text-slate-900 tracking-tight">
                {editingId ? "Настройка шаблона" : "Новый шаблон"}
              </h2>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-300 hover:text-slate-900 transition-colors"
              >
                <X size={28} strokeWidth={3} />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-10 space-y-8">
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] ml-4">
                  Имя в панели управления
                </label>
                <input
                  required
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  className="w-full bg-slate-50 border-2 border-transparent focus:border-cyan-100 focus:bg-white rounded-[1.5rem] px-8 py-4 outline-none font-bold text-slate-700 transition-all"
                  placeholder="Напр: Лифт_Новости_Блок_1"
                />
              </div>

              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] ml-4">
                    Тип виджета
                  </label>
                  <select
                    value={formData.widget_type}
                    onChange={(e) => handleTypeChange(e.target.value)}
                    className="w-full bg-slate-50 border-2 border-transparent rounded-[1.5rem] px-6 py-4 outline-none font-black text-slate-700 appearance-none cursor-pointer"
                  >
                    <option value="static">Статика</option>
                    <option value="news">Новости</option>
                    <option value="parking">Парковки</option>
                    <option value="storage">Кладовки</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] ml-4">
                    Заголовок (Экран)
                  </label>
                  <input
                    value={formData.title}
                    onChange={(e) =>
                      setFormData({ ...formData, title: e.target.value })
                    }
                    className="w-full bg-slate-50 border-2 border-transparent focus:border-cyan-100 focus:bg-white rounded-[1.5rem] px-8 py-4 outline-none font-bold"
                    placeholder="Напр: ОБЪЯВЛЕНИЕ"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase text-slate-400 tracking-[0.2em] ml-4">
                  {formData.widget_type === "static"
                    ? "Текст сообщения"
                    : "URL источника данных"}
                </label>
                <textarea
                  required
                  value={formData.content}
                  onChange={(e) =>
                    setFormData({ ...formData, content: e.target.value })
                  }
                  rows={formData.widget_type === "static" ? 5 : 2}
                  className="w-full bg-slate-50 border-2 border-transparent focus:border-cyan-100 focus:bg-white rounded-[1.5rem] px-8 py-5 outline-none font-medium text-slate-600 leading-relaxed transition-all resize-none"
                  placeholder={
                    formData.widget_type === "static"
                      ? "Введите текст, который увидят жильцы..."
                      : "/api/v1/data/..."
                  }
                />
              </div>

              <div className="flex gap-4">
                {editingId && (
                  <button
                    type="button"
                    onClick={handleDelete}
                    className="p-5 bg-red-50 text-red-500 rounded-[1.5rem] hover:bg-red-500 hover:text-white transition-all shadow-sm"
                    title="Удалить шаблон"
                  >
                    <Trash2 size={24} />
                  </button>
                )}
                <button
                  type="submit"
                  disabled={isSaving}
                  className="flex-1 bg-[#1e293b] hover:bg-black text-white py-5 rounded-[1.5rem] font-black uppercase tracking-widest shadow-xl transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                >
                  {isSaving ? (
                    <Loader2 className="animate-spin" size={24} />
                  ) : editingId ? (
                    "Сохранить изменения"
                  ) : (
                    "Создать шаблон"
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
