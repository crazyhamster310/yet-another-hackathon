import { useEffect, useState } from "react";
import DisplayPlayer from "./components/DisplayPlayer";
import AdminPanel from "./components/AdminPanel";

export default function App() {
  const [currentPath, setCurrentPath] = useState(window.location.pathname);

  useEffect(() => {
    const onLocationChange = () => {
      setCurrentPath(window.location.pathname);
    };

    window.addEventListener("popstate", onLocationChange);

    const originalPushState = window.history.pushState;
    window.history.pushState = function (...args) {
      originalPushState.apply(this, args);
      onLocationChange();
    };

    return () => {
      window.removeEventListener("popstate", onLocationChange);
      window.history.pushState = originalPushState;
    };
  }, []);

  if (currentPath.startsWith("/player/")) {
    const slug = currentPath.split("/")[2];

    if (!slug) {
      return (
        <div className="flex h-screen items-center justify-center bg-red-50 text-red-600 font-bold font-sans">
          Ошибка: ID дисплея не указан в URL
        </div>
      );
    }

    return <DisplayPlayer slug={slug} />;
  }

  return <AdminPanel />;
}