-- BackendAPI.lua - HTTP Client for AI-Powered Features
-- Part of GoblinAI v2.0
-- Connects to goblin-clean-1/backend FastAPI server

GoblinAI.BackendAPI = {}
local Backend = GoblinAI.BackendAPI

Backend.baseURL = "http://localhost:5000"
Backend.isConnected = false
Backend.lastSync = 0

-- ============================================================================
-- HTTP Request Simulation (WoW Limitation Workaround)
-- ============================================================================

-- Note: WoW doesn't have native HTTP support in Lua
-- This is a simulation that prepares data for external upload
-- In production, use:
--   1. External app (Python/Electron) to poll SavedVariables
--   2. LibStub HTTP library (if available)
--   3. Manual export/import workflow

function Backend:SimulateHTTPRequest(endpoint, method, data, callback)
    -- Prepare request data
    local request = {
        url = self.baseURL .. endpoint,
        method = method or "GET",
        data = data,
        timestamp = time(),
    }
    
    -- Store in export queue
    if not GoblinAIDB.apiQueue then
        GoblinAIDB.apiQueue = {}
    end
    
    table.insert(GoblinAIDB.apiQueue, request)
    
    print("|cFFFFD700Goblin AI:|r API request queued: " .. endpoint)
    print("Run external sync tool to process queue")
    
    -- Simulate async callback with mock data
    if callback then
        C_Timer.After(0.5, function()
            -- Return mock success for now
            callback(true, {status = "queued"})
        end)
    end
end

-- ============================================================================
-- Market Prices (DBMarket Equivalent)
-- ============================================================================

function Backend:FetchMarketPrices(callback)
    -- Get current market prices for all items
    -- This replaces TSM's DBMarket
    
    self:SimulateHTTPRequest("/api/goblin/prices", "GET", nil, function(success, data)
        if success and data.prices then
            -- Store in local cache
            GoblinAIDB.marketPrices = data.prices
            GoblinAIDB.lastPriceUpdate = time()
            
            print("|cFFFFD700Goblin AI:|r Market prices updated")
            
            if callback then
                callback(true, data.prices)
            end
        else
            -- Use cached data
            if callback then
                callback(false, GoblinAIDB.marketPrices or {})
            end
        end
    end)
end

function Backend:GetMarketPrice(itemID)
    -- Get cached market price
    if not GoblinAIDB.marketPrices then
        return nil
    end
    
    return GoblinAIDB.marketPrices[itemID]
end

-- ============================================================================
-- AI Opportunities (ML-Powered Flip Detection)
-- ============================================================================

function Backend:FetchOpportunities(callback)
    -- Get AI-recommended flip opportunities from ML models
    
    self:SimulateHTTPRequest("/api/goblin/opportunities", "GET", nil, function(success, data)
        if success and data.opportunities then
            -- Store opportunities
            GoblinAIDB.opportunities = data.opportunities
            
            print("|cFFFFD700Goblin AI:|r " .. #data.opportunities .. " AI opportunities loaded")
            
            if callback then
                callback(true, data.opportunities)
            end
        else
            -- Return mock opportunities for testing
            local mockOpps = Backend:GetMockOpportunities()
            
            if callback then
                callback(false, mockOpps)
            end
        end
    end)
end

function Backend:GetMockOpportunities()
    -- Mock data for testing without server
    return {
        {
            itemID = 210814, -- Algari Mana Potion
            buyPrice = 45000, -- 4g 50s
            sellPrice = 12 0000, -- 12g
            profit = 75000, -- 7g 50s
            roi = 1.67, -- 167% return
            predictedDemand = "high",
            confidence = 0.92,
        },
        {
            itemID = 211515, -- Null Stone
            buyPrice = 180000, -- 18g
            sellPrice = 350000, -- 35g
            profit = 170000, -- 17g
            roi = 0.94,
            predictedDemand = "medium",
            confidence = 0.85,
        },
    }
end

-- ============================================================================
-- Scan Data Upload
-- ============================================================================

function Backend:UploadScanData(scanData, callback)
    -- Upload AH scan to server for ML training
    
    local payload = {
        timestamp = time(),
        realm = GetRealmName(),
        faction = UnitFactionGroup("player"),
        character = GoblinAI:GetPlayerID(),
        scan = scanData,
    }
    
    self:SimulateHTTPRequest("/api/goblin/scan", "POST", payload, function(success, data)
        if success then
            print("|cFFFFD700Goblin AI:|r Scan data uploaded to ML pipeline")
        end
        
        if callback then
            callback(success, data)
        end
    end)
end

-- ============================================================================
-- Market Trends & Predictions
-- ============================================================================

function Backend:FetchTrends(callback)
    -- Get ML-powered market trend predictions
    
    self:SimulateHTTPRequest("/api/goblin/trends", "GET", nil, function(success, data)
        if success and data.trends then
            GoblinAIDB.marketTrends = data.trends
            
            if callback then
                callback(true, data.trends)
            end
        else
            -- Mock trends
            local mockTrends = {
                {
                    itemID = 210814,
                    trend = "rising", -- rising, falling, stable
                    prediction = "spike_expected",
                    confidence = 0.78,
                    timeframe = "24h",
                },
            }
            
            if callback then
                callback(false, mockTrends)
            end
        end
    end)
end

-- ============================================================================
-- Portfolio Tracking
-- ============================================================================

function Backend:FetchPortfolio(callback)
    -- Get portfolio value across all characters
    
    self:SimulateHTTPRequest("/api/goblin/portfolio", "GET", nil, function(success, data)
        if success and data.portfolio then
            GoblinAIDB.portfolio = data.portfolio
            
            print("|cFFFFD700Goblin AI:|r Portfolio: " .. GoblinAI:FormatGold(data.portfolio.totalValue))
            
            if callback then
                callback(true, data.portfolio)
            end
        else
            -- Mock portfolio
            local mockPortfolio = {
                totalValue = 15000000, -- 1,500g
                todayProfit = 250000, -- 25g
                weekProfit = 1800000, -- 180g
                activeAuctions = 47,
                pendingSales = 8500000, -- 850g
            }
            
            if callback then
                callback(false, mockPortfolio)
            end
        end
    end)
end

-- ============================================================================
-- Sync Manager (Auto-sync with Server)
-- ============================================================================

function Backend:StartAutoSync()
    if self.syncTimer then
        return -- Already running
    end
    
    local interval = 300 -- 5 minutes
    
    self.syncTimer = C_Timer.NewTicker(interval, function()
        if GoblinAIDB.settings.useBackend then
            Backend:SyncAll()
        end
    end)
    
    print("|cFFFFD700Goblin AI:|r Auto-sync enabled (every " .. interval .. "s)")
end

function Backend:StopAutoSync()
    if self.syncTimer then
        self.syncTimer:Cancel()
        self.syncTimer = nil
        print("|cFFFFD700Goblin AI:|r Auto-sync disabled")
    end
end

function Backend:SyncAll()
    print("|cFFFFD700Goblin AI:|r Syncing with backend...")
    
    -- Fetch latest data
    self:FetchMarketPrices()
    self:FetchOpportunities()
    self:FetchPortfolio()
    
    -- Upload latest scan if available
    local lastScan = GoblinAI.Scanner:GetLastScan()
    if lastScan then
        self:UploadScanData(lastScan.data)
    end
    
    self.lastSync = time()
end

-- ============================================================================
-- External Sync Tool Instructions
-- ============================================================================

function Backend:ShowSyncInstructions()
    print("|cFFFFD700=== Goblin AI Backend Sync ===|r")
    print("WoW addons cannot make HTTP requests directly.")
    print("To enable AI features, run the sync tool:")
    print("")
    print("|cFF00FF001. Run:|r python goblin_sync.py")
    print("|cFF00FF002. Tool monitors:|r SavedVariables/GoblinAI.lua")
    print("|cFF00FF003. Processes:|r apiQueue requests")
    print("|cFF00FF004. Updates:|r opportunities, prices, portfolio")
    print("")
    print("SavedVariables location:")
    print("WTF/Account/<NAME>/SavedVariables/GoblinAI.lua")
    print("|cFFFFD700================================|r")
end

-- ============================================================================
-- Initialization
-- ============================================================================

-- Start auto-sync if backend enabled
if GoblinAIDB and GoblinAIDB.settings and GoblinAIDB.settings.useBackend then
    Backend:StartAutoSync()
end

print("|cFFFFD700Goblin AI:|r Backend API loaded - Ready for AI features")
print("Type |cFF00FF00/goblin sync|r for setup instructions")
