
import React, { useContext, useEffect, useState } from "react";
import Navbar from "../components/navbar";
import { SelectContext } from "../provider/selectProvider";

interface TableRow {
  keyword: string;
  url: string;
  similarity: number;
}

const ArticleTableForm: React.FC = () => {
  const context = useContext(SelectContext);
  const [selectedRows, setSelectedRows] = useState<boolean[]>(
    context?.insertedLinks?.map(() => true) || []
  );

  // Sync selectedRows when insertedLinks changes
  useEffect(() => {
    setSelectedRows(context?.insertedLinks?.map(() => true) || []);
  }, [context?.insertedLinks]);


  const toggleRowSelection = (index: number) => {
  const newSelectedRows = [...selectedRows];
  newSelectedRows[index] = !newSelectedRows[index];
  setSelectedRows(newSelectedRows);

  const parser = new DOMParser();
  const doc = parser.parseFromString(context?.html_format_article || "", "text/html");

  // Step 1: Remove all internal anchor tags (clean slate)
  const allAnchors = doc.querySelectorAll("a");
  allAnchors.forEach(anchor => {
    const text = anchor.textContent;
    if (text) {
      const span = document.createTextNode(text);
      anchor.replaceWith(span);
    }
  });

  // Step 2: Get plain HTML without any internal anchors
  let cleanHTML = doc.body.innerHTML;

  // Step 3: Re-insert only selected links (no duplicates)
  const linksToInclude = context?.insertedLinks?.filter((_, i) => newSelectedRows[i]) || [];

  // Insert links only for the first non-wrapped instance
  linksToInclude.forEach(({ keyword, url }) => {
    const escapedKeyword = keyword.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
    const regex = new RegExp(`(?<!<[^>]*?)\\b(${escapedKeyword})\\b(?![^<]*?>)`, 'i');
    cleanHTML = cleanHTML.replace(regex, `<a href="${url}" target="_blank">$1</a>`);
  });

  if (context?.setHtmlFormatArticle) {
    context.setHtmlFormatArticle(cleanHTML);
  }
};

  const downloadArticle = () => {
    const blob = new Blob([context?.html_format_article as string], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "article.txt";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const downloadTable = () => {
    const head = "Keyword,Related Link,Similarity\n";
    const rows = context?.insertedLinks
      ?.filter((_, index: number) => selectedRows[index])
      .map((row: TableRow) => `${row.keyword},${row.url},${row.similarity}`)
      .join("\n");

    const csvContent = head + rows;
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "related_links.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const download = () => {
    downloadArticle();
    downloadTable();
  };

  return (
    <>
    <section className="w-full min-h-screen flex justify-center">
      <div className="mx-auto w-full max-w-screen-xl h-[600px] px-12 flex justify-around items-center flex-col">
        <Navbar />

        <div className="w-full">
          <h2 className="block font-medium text-xl">Article</h2>
          <div
            className="w-full border-2 rounded-lg px-3 py-2 min-h-[300px]"
            contentEditable={false}
            dangerouslySetInnerHTML={{ __html: context?.html_format_article || "" }}
          ></div>
        </div>

        <div className="w-full flex flex-col gap-3">
          <h2 className="block font-bold text-xl">Table</h2>
          <div className="overflow-x-auto rounded border">
            <table className="w-full border-collapse table-auto text-sm">
              <thead>
                <tr className="bg-[#7F7194] h-12 text-white">
                  <th className="p-2">Select</th>
                  <th className="p-2">Keyword</th>
                  <th className="p-2">Related Link</th>
                  <th className="p-2">Similarity</th>
                </tr>
              </thead>
              <tbody className="w-full h-fit">
                {context?.insertedLinks?.length ? (
                  context.insertedLinks.map((row: TableRow, index: number) => (
                    <tr key={index} className="border-b-2 w-full h-8">
                      <td className="w-1/6 p-2 border-r-2">
                        <input
                          type="checkbox"
                          checked={selectedRows[index]}
                          onChange={() => toggleRowSelection(index)}
                          className="h-4 w-4"
                        />
                      </td>
                      <td className="w-1/3 p-2 border-r-2">{row.keyword}</td>
                      <td className="w-1/3 p-2">{row.url}</td>
                      <td className="w-1/6 p-2">{row.similarity}</td>
                    </tr>
                  ))
                ) : (
                  <tr className="border-b-2 w-full h-8">
                    <td className="w-1/2 p-2" colSpan={4}>
                      No Relevant Links Found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <button
            onClick={download}
            className="block self-center w-48 h-14 text-center leading-14 hover:shadow-md rounded-lg text-lg bg-[#7F7194] text-white font-bold"
          >
            Download Table
          </button>
        </div>
      </div>
    </section>
    </>
  );
};

export default ArticleTableForm;