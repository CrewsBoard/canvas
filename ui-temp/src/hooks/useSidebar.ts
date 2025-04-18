'use client';

import { useEffect } from 'react';
import { useSidebar as useShadcnSidebar } from '@/components/ui/sidebar';

export function useSidebar() {
  const { setOpen } = useShadcnSidebar();

  useEffect(() => {
    const handleMouseEnter = () => {
      const sidebarElement = document.querySelector('[data-sidebar="sidebar"]');
      if (sidebarElement) {
        setOpen(true);
      }
    };

    const handleMouseLeave = () => {
      const sidebarElement = document.querySelector('[data-sidebar="sidebar"]');
      if (sidebarElement) {
        setOpen(false);
      }
    };

    // Find the sidebar element
    const sidebarElement = document.querySelector('[data-sidebar="sidebar"]');

    if (sidebarElement) {
      sidebarElement.addEventListener('mouseenter', handleMouseEnter);
      sidebarElement.addEventListener('mouseleave', handleMouseLeave);
    }

    return () => {
      if (sidebarElement) {
        sidebarElement.removeEventListener('mouseenter', handleMouseEnter);
        sidebarElement.removeEventListener('mouseleave', handleMouseLeave);
      }
    };
  }, [setOpen]);

  return null;
}
