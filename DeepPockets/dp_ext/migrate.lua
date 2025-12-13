DeepPockets.Migrate = DeepPockets.Migrate or {}

function DeepPockets.Migrate.Ensure()
  DeepPocketsDB = DeepPocketsDB or {}
  local db = DeepPocketsDB

  if not db.version or db.version < 1 then
    db.version = 1
  end

  db.settings = db.settings or { debug = false }
  db.inventory = db.inventory or {}
  db.index = db.index or { by_item = {}, by_category = {} }
  db.meta = db.meta or {}

  local _, build, _, toc = GetBuildInfo()
  db.meta.build = build
  db.meta.toc = toc
end
