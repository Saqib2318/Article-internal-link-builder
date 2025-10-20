import React, { createContext, useEffect, useState } from "react";

// Define the shape of the context
export interface SelectMode {
  selectAction: string;
  userName?: string;
  password?: string;
  technology?: string;
  url?: string;
  NumLinks: number;
  Article: string; // Original plain text article
  original_article?: string; // Added to store the original article
  modifiedarticle?: string;
  insertedLinks?: { similarity: number; keyword: string; url: string }[];
  html_format_article?: string;
  setState?: React.Dispatch<React.SetStateAction<SelectMode>>;
  setHtmlFormatArticle?: (html: string) => void; // Added to update html_format_article
}

// Create context with initial empty/default values
export const SelectContext = createContext<SelectMode>({
  selectAction: "wordpress",
  NumLinks: 0,
  Article: "",
});

// LocalStorage key
const STORAGE_KEY = "select-mode-context";

// Provider component
interface SelectProviderProps {
  children: React.ReactNode;
}

export const SelectProvider: React.FC<SelectProviderProps> = ({ children }) => {
  // Load from localStorage if available
  const getInitialState = (): SelectMode => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch {
        return {
          selectAction: "wordpress",
          NumLinks: 0,
          Article: "",
        };
      }
    }
    return {
      selectAction: "wordpress",
      NumLinks: 0,
      Article: "",
    };
  };

  const [state, setState] = useState<SelectMode>(getInitialState);

  // Function to update html_format_article
  const setHtmlFormatArticle = (html: string) => {
    setState((prev) => ({ ...prev, html_format_article: html }));
  };

  // Save to localStorage on every state change
  useEffect(() => {
    const { setState: _, setHtmlFormatArticle: __, ...persisted } = state; // Remove setState and setHtmlFormatArticle from being saved
    localStorage.setItem(STORAGE_KEY, JSON.stringify(persisted));
  }, [state]);

  return (
    <SelectContext.Provider value={{ ...state, setState, setHtmlFormatArticle }}>
      {children}
    </SelectContext.Provider>
  );
};