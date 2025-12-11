export type Gradient = string;
export type Color = string;
export type Shadow = string;

export interface ThemeBackground {
  image: string;
  vignette?: Gradient;
  overlay?: Gradient;
}

export interface ThemeGlow {
  soft: string;
  strong: string;
  pulse?: string;
}

export interface ThemeRarity {
  border: Color;
  text: Color;
  glow: string;
}

export interface Theme {
  colors: Record<string, Color>;
  gradients: Record<string, Gradient>;
  rarity: Record<string, ThemeRarity>;
  backgrounds: Record<string, ThemeBackground>;
  glows: Record<string, ThemeGlow>;
  layers: Record<string, number>;
}
