import InfoModel from "./info-model"


const Navbar = () => {
  return (
        <nav className="w-full h-[120px] flex justify-between
         items-center">
            <img src="logo.png" alt="" className="w-24 h-24 object-cover" />
            <h2 className="text-xl font-bold ">LINK MASTER</h2>
            <div className="w-1/3 visibility-hidden"></div>
        </nav>
  )
}

export default Navbar