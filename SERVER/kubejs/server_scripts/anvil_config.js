const ForgeRegistries = Java.loadClass("net.minecraftforge.registries.ForgeRegistries")
const ResourceLocation = Java.loadClass("net.minecraft.resources.ResourceLocation")
const CompoundTag = Java.loadClass("net.minecraft.nbt.CompoundTag")
const ListTag = Java.loadClass("net.minecraft.nbt.ListTag")
const Component = Java.loadClass("net.minecraft.network.chat.Component")
const ItemStack = Java.loadClass("net.minecraft.world.item.ItemStack")

NativeEvents.onEvent(Java.loadClass("net.minecraftforge.event.AnvilUpdateEvent"), event => {
    var left = event.getLeft()
    var right = event.getRight()
    var leftId = left.getItem().toString()
    var rightId = right.isEmpty() ? "empty" : right.getItem().toString()
    var name = event.getName()
    var isEnchantedBook = rightId === "enchanted_book"
    var isNameOnly = rightId === "empty"
    var finalCost = 1

    if (!isEnchantedBook && !isNameOnly) {
        event.setCanceled(true)
        return
    }

    var isValidTarget = leftId === "enchanted_book" ||
        left.getTags().anyMatch(t => t.location().toString() === "forge:tools") ||
        left.getTags().anyMatch(t => t.location().toString() === "forge:armors")

    if (isEnchantedBook && !isValidTarget) {
        event.setCanceled(true)
        return
    }

    if (isEnchantedBook) {
        var output = left.copy()
        var isLeftBook = leftId === "enchanted_book"
        var targetKey = isLeftBook ? "StoredEnchantments" : "Enchantments"
        var bookTag = right.getOrCreateTag()
        var applied = false
        if (bookTag.contains("StoredEnchantments")) {
            var storedList = bookTag.getList("StoredEnchantments", 10)
            for (var i = 0; i < storedList.size(); i++) {
                var entry = storedList.getCompound(i)
                var enchId = entry.getString("id")
                var enchLvl = entry.getShort("lvl")
                var enchantment = ForgeRegistries.ENCHANTMENTS.getValue(new ResourceLocation(enchId))
                if (!enchantment) continue
                // Only enchantments the item could get at an enchanting table or vanilla anvil
                if (!isLeftBook && !enchantment.canEnchant(left)) continue
                var tag = output.getOrCreateTag()
                var enchList = tag.contains(targetKey) ? tag.getList(targetKey, 10) : new ListTag()
                var existingIndex = -1
                var compatible = true
                for (var j = 0; j < enchList.size(); j++) {
                    var otherId = enchList.getCompound(j).getString("id")
                    if (otherId === enchId) {
                        existingIndex = j
                        continue
                    }
                    var other = ForgeRegistries.ENCHANTMENTS.getValue(new ResourceLocation(otherId))
                    if (other && !enchantment.isCompatibleWith(other)) compatible = false
                }
                if (!compatible) continue
                var existingLevel = existingIndex >= 0 ? enchList.getCompound(existingIndex).getShort("lvl") : 0
                // Two equal levels combine into the next one, up to the enchantment's maximum
                var finalLevel = (existingLevel === enchLvl && enchLvl < enchantment.getMaxLevel()) ? enchLvl + 1 : Math.max(existingLevel, enchLvl)
                if (finalLevel <= existingLevel) continue
                finalCost += finalLevel * 10
                if (existingIndex >= 0) enchList.remove(existingIndex)
                var enchEntry = new CompoundTag()
                enchEntry.putString("id", enchId)
                enchEntry.putShort("lvl", finalLevel)
                enchList.add(enchEntry)
                tag.put(targetKey, enchList)
                applied = true
            }
        }
        if (!applied) {
            event.setCanceled(true)
            return
        }
        if (name && name !== "") {
            output.setHoverName(Component.literal(name))
        }
        event.setOutput(output)
        event.setCost(finalCost)
        event.setMaterialCost(0)
    }
})