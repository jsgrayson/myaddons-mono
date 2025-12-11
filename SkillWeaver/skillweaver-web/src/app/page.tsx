export default function Home() {
    return (
        <main className="min-h-screen p-8">
            <div className="max-w-6xl mx-auto">
                {/* Navigation */}
                <nav className="flex justify-between items-center mb-12 py-4 border-b border-gray-700">
                    <div className="font-bold text-xl text-blue-400">SkillWeaver</div>
                    <div className="space-x-6">
                        <a href="#" className="text-gray-300 hover:text-white transition-colors">Dashboard</a>
                        <a href="#" className="text-gray-300 hover:text-white transition-colors">Talents</a>
                        <a href="#" className="text-gray-300 hover:text-white transition-colors">Gear</a>
                        <a href="http://localhost:5001" target="_blank" className="text-blue-400 hover:text-blue-300 font-semibold transition-colors">Holocron ↗</a>
                    </div>
                </nav>

                {/* Header */}
                <header className="mb-12">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent mb-4">
                        SkillWeaver
                    </h1>
                    <p className="text-xl text-gray-400">
                        AI-Powered Character Optimization for World of Warcraft
                    </p>
                </header>

                {/* Hero Section */}
                <section className="bg-gray-800 rounded-lg p-8 mb-8">
                    <h2 className="text-3xl font-bold mb-4">Welcome to SkillWeaver</h2>
                    <p className="text-gray-300 mb-6">
                        Import your characters, get optimal talent builds, and maximize your performance
                        in Raids, Mythic+, PvP, and Delves.
                    </p>

                    <button className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition-colors">
                        Connect Battle.net
                    </button>
                </section>

                {/* Features Grid */}
                <div className="grid md:grid-cols-3 gap-6">
                    <div className="bg-gray-800 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2 text-blue-400">Talent Planner</h3>
                        <p className="text-gray-400">
                            Get optimal talent builds for every spec and content type
                        </p>
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2 text-purple-400">Gear Optimizer</h3>
                        <p className="text-gray-400">
                            Stat weights and BiS recommendations for your character
                        </p>
                    </div>

                    <div className="bg-gray-800 p-6 rounded-lg">
                        <h3 className="text-xl font-bold mb-2 text-green-400">Gold Making</h3>
                        <p className="text-gray-400">
                            Integrated with Goblin AI for profession recommendations
                        </p>
                    </div>
                </div>

                {/* Footer */}
                <footer className="mt-12 text-center text-gray-500">
                    <p>SkillWeaver &copy; 2024 | Powered by Blizzard API</p>
                </footer>
            </div>
        </main>
    )
}
