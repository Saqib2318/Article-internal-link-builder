import { Link } from "react-router"
const GetStarted = () => {
  return (
    <section className="w-full min-h-screen bg-gray-400">
        <div className="mx-auto w-full h-[600px] px-12 flex justify-around items-center flex-col">
            <img src="logo.png" alt="" className="w-[500px] h-[400px] object-cover" />
            <div className="w-full text-center h-1/3 -mt-12">
                <h1 className="text-6xl font-bold text-black capitalize">LINK MASTER</h1>
                <p className="text-5xl font-semibold">Automate Your Internal Linking Process</p>
            </div>
            <div>
             <Link to={'/select-action'}><span className="block w-48 h-14 text-center leading-14 hover:shadow-md  rounded-lg text-lg bg-[#7F7194] text-white font-bold">Get Started</span></Link>   
            </div>
        </div>
    </section>
  )
}

export default GetStarted