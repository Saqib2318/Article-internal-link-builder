import { useContext } from "react";
import Navbar from "../components/navbar";
import { SelectContext } from "../provider/selectProvider";
import { Link } from "react-router";

const SelectAction = () => {
    const selectMode = useContext(SelectContext)
  return (
    <section className="w-full min-h-screen bg-gray-50 flex justify-center">
      <div className="w-full max-w-[1220px] h-[1000px] px-4 md:px-12 mx-auto flex flex-col items-center gap-2">
        {/* Navbar at the top */}
        <Navbar />
        {/* Add your action buttons or content below */}
        <div className="w-full flex h-3/4 items-around justify-center gap-6">
           <img src="choose-action.png
           " alt="" className="w-1/2 h-full object-cover" /> 
          <div className="flex flex-col gap-6 w-1/2 h-full justify-center items-center">
            
            <div className={`w-1/3 h-48 rounded-2xl shadow-xl cursor-pointer ${selectMode.selectAction == 'wordpress' && "shadow-violet-300"}`} onClick={() => selectMode.setState?.({ ...selectMode, selectAction: "wordpress" })}>
                <img src="wordpress.png" alt="" className="w-full h-48 object-full" />
            </div>
            <div className={`w-1/3 h-48 rounded-xl shadow-xl cursor-pointer ${selectMode.selectAction !== 'wordpress' && "shadow-violet-300"}`} onClick={() => selectMode.setState?.({ ...selectMode, selectAction: "custom" })}>
                <img src="customWeb.png" alt="" className="w-full h-48 object-full" />
            </div>
          </div>
        </div>
        <div className="w-full h-1/5 flex justify-center items-center">
        <Link to={'/Form-Action'}><span className="block w-48 h-14 text-center leading-14 hover:shadow-md  rounded-lg text-lg bg-[#7F7194] text-white font-bold">Next Step</span></Link>   
        </div>
      </div>
    </section>
  );
};

export default SelectAction;
