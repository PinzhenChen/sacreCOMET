from comet import download_model, load_from_checkpoint
import torch
import torch.quantization

model_path = download_model("Unbabel/wmt22-comet-da")
model = load_from_checkpoint(model_path)

def test_model(model):
    data = [
        {
            "src": "Dem Feuer konnte Einhalt geboten werden",
            "mt": "The fire could be stopped",
            "ref": "They were able to control the fire."
        },
        {
            "src": "Schulen und Kindergärten wurden eröffnet.",
            "mt": "Schools and kindergartens were open",
            "ref": "Schools and kindergartens opened"
        }
    ]
    return model.predict(data, batch_size=8, gpus=0)



model_qint8 = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8,
    inplace=False
)


# ('scores', [0.8385584354400635, 0.971725583076477]), ('system_score', 0.9051420092582703)
print("F32:", test_model(model))
# ('scores', [0.8789860606193542, 0.8911461234092712]), ('system_score', 0.8850660920143127)
print("I8: ", test_model(model_qint8))