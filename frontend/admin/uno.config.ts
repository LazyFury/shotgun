// uno.config.ts
import {
    defineConfig,
    presetAttributify,
    presetIcons,
    presetTypography,
    presetUno,
    presetWebFonts,
    transformerDirectives,
    transformerVariantGroup
  } from 'unocss'

export default defineConfig({
  presets: [
    presetAttributify({ /* preset options */}),
    presetUno(),
    // ...custom presets
    presetIcons(),
    presetTypography(),
    presetWebFonts(),
  ],
  transformers:[
    transformerDirectives(),
    transformerVariantGroup()
  ],
  theme:{
    colors:{
        "bg-primary":"#1a1d48",
        "primary": '#0F609B',
        secondary: '#0F609B',
        accent: '#F59E0B',
        danger: '#DC2626',
        success: '#10B981',
        warning: '#F59E0B',
        info: '#3B82F6',
    }
  },
  shortcuts:{
    "flex-row-btn":"flex flex-row items-center gap-1"
  }
})
