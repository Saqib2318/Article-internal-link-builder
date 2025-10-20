import React, { useContext, useState } from "react";
import { SelectContext } from "../provider/selectProvider";
import Navbar from "../components/navbar";
import { useNavigate } from "react-router";
import ToastMessage  from "../components/info-model";

const AutoInternalToolForm: React.FC = () => {
  const context = useContext(SelectContext);
  const isWordPress = context.selectAction === "wordpress";
  const [isloading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [technology, setTechnology] = useState(context.technology || "");
  const [url, setUrl] = useState(context.url || "");
  const [numLinks, setNumLinks] = useState(context.NumLinks || 0);
  const [article, setArticle] = useState(context.Article || "");
  const [toastMessage, setToastMessage] = useState("");
  const navigate = useNavigate()
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url || !article || numLinks <= 0) {
      setToastMessage("Please fill in all fields correctly.");
      return;
    }else if (!url.startsWith("http://") && !url.startsWith("https://")) {
      setToastMessage("URL must start with http:// or https://");
      return;
    }
    context.setState?.(prev => ({
      ...prev,
      technology: isWordPress ? undefined : technology,
      url,
      NumLinks: Number(numLinks),
      Article: article,
    }));
    try {
      setIsLoading(true);
      setIsError(false);
      let sendRequest = await fetch("http://127.0.0.1:8000/build-links",{
        method:"POST",
        headers:{
          'content-type':"application/json"
        },
        body:JSON.stringify({
          content:context.Article,
          main_url:url,
          num_links:context.NumLinks,
          plateform:context.selectAction,
          wp_base_url:context.selectAction === "wordpress" && url,
        })
      })
      let response = await sendRequest.json()
      if(!sendRequest.ok){
        setIsError(true);
        setToastMessage(response?.detail || "An error occurred while processing your request.");
      }else{
        context.setState?.((prev)=>{return {
          ...prev,
          modifiedarticle:response?.modified_content,
          insertedLinks:response?.inserted_links,
          html_format_article:response?.html_format_content as string
        }})

        navigate('/result-article')
      }
    } catch (error) {
      console.log(`error is occuring ${error}`)
      setIsError(true);
      setToastMessage(error instanceof Error ? error.message : "An unexpected error occurred.");
    }finally {
      setIsLoading(false);
      setTimeout(() => {
        setToastMessage("");
      }, 5000);
    }
  };
  return (
    <section className="w-full h-full flex justify-center">
    <div className="w-full max-w-[1220px] max-h-screen mx-auto px-12 bg-white rounded-xl my-1">
      {/* Header */}
      <Navbar/>

      {/* Form */}
      <form onSubmit={handleSubmit} className="space-y-4 w-full h-[580px] flex flex-col gap-4">
        
        <div className="flex items-center justify-between w-full h-12">
          <label className="w-1/5 font-bold text-2xl">URL</label>
          <input
            type="text"
            value={url}
            onChange={e => setUrl(e.target.value)}
            className="flex-1 outline-none border-2 rounded-md 4/5 h-full p-2"
            placeholder="Enter your URL"
          />
        </div>

        <div className="flex items-center justify-between w-full h-12">
          <label className="w-1/5 font-bold text-2xl">No of Links</label>
          <input
            type="number"
            value={numLinks}
            max={20}
            min={1}
            onChange={e => parseInt(e.target.value) > 20 ? setNumLinks(20):setNumLinks(parseInt(e.target.value))}
            className="flex-1 outline-none border-2 rounded-md w-4/5 h-full p-2"
            placeholder="Enter number of links"
          />
        </div>

        <div className="flex flex-col">
          <label className="font-bold text-2xl mb-1">Article</label>
          <textarea
            value={article}
            onChange={e => setArticle(e.target.value)}
            className="border-2  outline-none rounded-xl resize-none overflow-y-scroll px-4 py-1 min-h-[300px]"
            placeholder="Write your article here..."
          />
        </div>

        <div className="flex justify-center pt-2">
          <button
            type="submit"
            className={`block w-48 h-14 text-center leading-14  hover:shadow-md rounded-lg text-lg bg-[#7F7194]  text-white font-bold transition cursor-pointer` + (isloading ? " cursor-not-allowed opacity-50" : "") + (isError ? " bg-red-500 hover:bg-red-600" : "")}
          >
            {isloading ? "Loading..." : isError ? "Retry" : "Submit Now"}
          </button>
        </div>
      </form>
      {/* Toast Message */}
      {toastMessage && (
        <ToastMessage
          message={toastMessage}
          onClose={() => setToastMessage("")}
        />
      )}
    </div>
</section>
  );
};

export default AutoInternalToolForm;
